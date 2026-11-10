import json
import logging
from typing import List, Dict, Any, Optional, Tuple
import httpx
from backend.app.config import settings
from backend.app.schemas.claim import EvidenceRecordSchema, RumourDNASchema

logger = logging.getLogger(__name__)

class GeminiAIService:
    """
    Configurable AI Evidence Interpretation Provider using Google's Gemini Developer API.
    Operates strictly as an interpretation assistant over retrieved snippets.
    
    Safeguards:
    - Never invents URLs, publishers, or quotes.
    - Explicitly labels evidence as search snippets.
    - Gracefully falls back to rule-based evaluation on missing key, timeout, 429 quota, or format errors.
    """
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key if api_key is not None else settings.GEMINI_API_KEY
        self.model = model or settings.GEMINI_MODEL or "gemini-3.5-flash"
        self.timeout = 12.0  # seconds (allows headroom for free-tier response generation)

    def is_available(self) -> bool:
        return bool(self.api_key and self.api_key.strip())

    def analyze_evidence(
        self,
        dna: RumourDNASchema,
        evidence: List[EvidenceRecordSchema]
    ) -> Tuple[Optional[Dict[str, Any]], bool, str]:
        """
        Sends the claim assertion and retrieved search snippets to Gemini.
        Returns: (parsed_analysis_dict, success_bool, status_message)
        """
        if not self.is_available():
            return None, False, "AI provider inactive: GEMINI_API_KEY is not configured. Using rule-based semantic analysis."

        if not evidence:
            return None, False, "No evidence records to interpret."

        # Prepare evidence payloads with clear snippet labelling
        records_payload = []
        for idx, rec in enumerate(evidence):
            records_payload.append({
                "index": idx,
                "publisher": rec.publisher,
                "title": rec.title,
                "url": rec.url,
                "reliability_score": rec.reliability_score,
                "search_snippet": rec.excerpt
            })

        system_instruction = (
            "You are a rigorous evidence evaluation engine for Evolution Tracker 2.0. "
            "Analyze the given factual assertion against retrieved search snippets. "
            "CRITICAL SAFEGUARDS: "
            "1. You only have access to short search snippets, NOT full articles. Never imply you read the full article. "
            "2. Do not invent sources, URLs, or facts. "
            "3. For each snippet, classify it strictly as: 'SUPPORTING', 'CONTRADICTING', 'CONTEXTUAL', or 'IRRELEVANT'. "
            "   - SUPPORTING: Directly confirms the specific factual assertion. "
            "   - CONTRADICTING: Directly refutes, contradicts, exhibits reversed polarity/antonyms, or debunks the assertion. "
            "   - CONTEXTUAL: Discusses the subject but does not confirm or refute the specific assertion. "
            "   - IRRELEVANT: Unrelated topic or off-topic source. "
            "4. Determine the overall verdict strictly as one of: 'LIKELY TRUE', 'LIKELY FALSE', 'MIXED / PARTIALLY TRUE', 'UNVERIFIED'. "
            "5. Determine confidence level strictly as: 'HIGH', 'MEDIUM', 'LOW'. "
            "6. Output MUST be valid JSON adhering to the required schema."
        )

        user_content = {
            "claim_text": dna.normalized_text,
            "factual_assertion": dna.factual_assertion,
            "subject": dna.subject,
            "is_negated": getattr(dna, "is_negated", False),
            "evidence_snippets": records_payload
        }

        request_body = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": (
                                f"{system_instruction}\n\n"
                                f"INPUT DATA (Analyze these snippets):\n{json.dumps(user_content, indent=2)}\n\n"
                                "Return JSON with format:\n"
                                "{\n"
                                '  "evaluations": [\n'
                                '    {\n'
                                '      "index": 0,\n'
                                '      "classification": "SUPPORTING|CONTRADICTING|CONTEXTUAL|IRRELEVANT",\n'
                                '      "reason": "1-2 sentence explanation",\n'
                                '      "supporting_quote": "Exact short quotation from the snippet or null",\n'
                                '      "is_duplicate_of": null\n'
                                '    }\n'
                                '  ],\n'
                                '  "verdict": "LIKELY TRUE|LIKELY FALSE|MIXED / PARTIALLY TRUE|UNVERIFIED",\n'
                                '  "confidence": "HIGH|MEDIUM|LOW",\n'
                                '  "verdict_reason": "Clear explanation of the main reason for the verdict.",\n'
                                '  "truth_explanation": "Objective summary of what documented records establish."\n'
                                "}"
                            )
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.0,
                "responseMimeType": "application/json"
            }
        }

        # Call Gemini REST endpoint
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                res = client.post(url, json=request_body)
                
                # Check for 404 or 503 on model name, retry with candidate fallback models
                if res.status_code in (404, 503):
                    candidate_fallbacks = ["gemini-3.1-flash-lite", "gemini-3-flash-preview", "gemini-3.5-flash"]
                    for fb in candidate_fallbacks:
                        if fb != self.model:
                            fallback_url = f"https://generativelanguage.googleapis.com/v1beta/models/{fb}:generateContent?key={self.api_key}"
                            fb_res = client.post(fallback_url, json=request_body)
                            if fb_res.status_code == 200:
                                res = fb_res
                                break

                if res.status_code == 429:
                    logger.warning("Gemini API rate limit or quota exceeded (HTTP 429). Falling back to rule-based analysis.")
                    return None, False, "Gemini quota or rate limit reached. Analysis executed via rule-based engine."

                if res.status_code != 200:
                    logger.warning(f"Gemini API returned error status {res.status_code}: {res.text[:200]}")
                    return None, False, f"AI provider returned status {res.status_code}. Analysis executed via rule-based engine."

                data = res.json()
                candidates = data.get("candidates", [])
                if not candidates:
                    return None, False, "AI response contained no candidate outputs. Using rule-based fallback."

                raw_text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                parsed = json.loads(raw_text)

                # Validate response structure
                if not isinstance(parsed, dict) or "evaluations" not in parsed:
                    return None, False, "AI response failed structural schema validation. Using rule-based fallback."

                # Normalize evaluations
                normalized_evals = []
                for ev_item in parsed.get("evaluations", []):
                    cls_raw = str(ev_item.get("classification", "CONTEXTUAL")).upper().strip()
                    if "SUPPORT" in cls_raw:
                        cls_norm = "supporting"
                    elif "CONTRADICT" in cls_raw:
                        cls_norm = "contradictory"
                    elif "IRRELEVANT" in cls_raw:
                        cls_norm = "irrelevant"
                    else:
                        cls_norm = "contextual"
                    
                    normalized_evals.append({
                        "index": ev_item.get("index", 0),
                        "classification": cls_norm,
                        "reason": ev_item.get("reason", "Evaluated by AI interpretation engine."),
                        "supporting_quote": ev_item.get("supporting_quote"),
                        "is_duplicate_of": ev_item.get("is_duplicate_of")
                    })

                parsed["evaluations"] = normalized_evals

                # Validate suggested verdict
                verdict_raw = str(parsed.get("verdict", "UNVERIFIED")).upper().strip()
                if "TRUE" in verdict_raw and "PARTIAL" not in verdict_raw and "MIXED" not in verdict_raw:
                    parsed["verdict"] = "LIKELY TRUE"
                elif "FALSE" in verdict_raw:
                    parsed["verdict"] = "LIKELY FALSE"
                elif "MIXED" in verdict_raw or "PARTIAL" in verdict_raw:
                    parsed["verdict"] = "MIXED / PARTIALLY TRUE"
                else:
                    parsed["verdict"] = "UNVERIFIED"

                # Validate confidence
                conf_raw = str(parsed.get("confidence", "LOW")).upper().strip()
                if "HIGH" in conf_raw:
                    parsed["confidence"] = "HIGH"
                elif "MED" in conf_raw:
                    parsed["confidence"] = "MEDIUM"
                else:
                    parsed["confidence"] = "LOW"

                return parsed, True, "AI-assisted interpretation active (Google Gemini)"

        except httpx.TimeoutException:
            logger.warning("Gemini API call timed out. Falling back to rule-based engine.")
            return None, False, "AI interpretation timed out (>7s). Falling back to rule-based engine."
        except json.JSONDecodeError:
            logger.warning("Failed to decode Gemini JSON response. Falling back to rule-based engine.")
            return None, False, "Invalid JSON received from AI provider. Falling back to rule-based engine."
        except Exception as e:
            logger.warning(f"Unexpected error calling Gemini API: {str(e)}")
            return None, False, f"AI connection error ({type(e).__name__}). Falling back to rule-based engine."

ai_service = GeminiAIService()
