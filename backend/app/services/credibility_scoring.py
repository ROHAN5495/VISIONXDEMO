import re
from typing import List, Dict, Any, Optional, Tuple
from backend.app.schemas.claim import EvidenceRecordSchema, ScoreBreakdownSchema, RumourDNASchema

def compute_text_similarity(text1: str, text2: str) -> float:
    """Calculates Jaccard token similarity to detect identical or syndicated reports."""
    w1 = set(re.findall(r'\b[a-zA-Z]{3,}\b', text1.lower()))
    w2 = set(re.findall(r'\b[a-zA-Z]{3,}\b', text2.lower()))
    if not w1 or not w2:
        return 0.0
    intersection = len(w1 & w2)
    union = len(w1 | w2)
    return intersection / union if union > 0 else 0.0

def select_key_excerpts(
    evidence: List[EvidenceRecordSchema],
    verdict: str,
    max_count: int = 3
) -> List[Dict[str, Any]]:
    """
    Selects a small number of the most relevant evidence excerpts for the main investigation summary.
    Prioritizes records that directly substantiate the verdict.
    """
    if not evidence:
        return []

    supporting = [e for e in evidence if e.classification == "supporting"]
    contradictory = [e for e in evidence if e.classification == "contradictory"]
    contextual = [e for e in evidence if e.classification == "contextual"]

    selected: List[EvidenceRecordSchema] = []

    if verdict == "LIKELY FALSE":
        # Prioritize contradictory records
        selected = sorted(contradictory, key=lambda x: x.reliability_score, reverse=True)[:max_count]
        if len(selected) < max_count and supporting:
            selected.append(supporting[0])
    elif verdict == "LIKELY TRUE":
        # Prioritize supporting records
        selected = sorted(supporting, key=lambda x: x.reliability_score, reverse=True)[:max_count]
        if len(selected) < max_count and contradictory:
            selected.append(contradictory[0])
    elif verdict == "MIXED / PARTIALLY TRUE":
        # Show both supporting and contradictory
        if contradictory:
            selected.append(contradictory[0])
        if supporting:
            selected.append(supporting[0])
        remaining = [e for e in evidence if e not in selected]
        if remaining and len(selected) < max_count:
            selected.append(remaining[0])
    else:
        # Unverified - show up to max_count contextual records
        selected = sorted(contextual or evidence, key=lambda x: x.reliability_score, reverse=True)[:max_count]

    result = []
    for s in selected:
        quote = getattr(s, "supporting_quote", None) or s.excerpt
        if len(quote) > 220:
            quote = quote[:217] + "..."
            
        result.append({
            "publisher": s.publisher,
            "title": s.title,
            "url": s.url,
            "excerpt": quote,
            "classification": s.classification,
            "reliability_score": s.reliability_score,
            "relevance_reason": s.relevance_reason,
            "is_snippet": True,
            "is_independent": s.is_independent
        })
    return result

def calculate_evidence_score(
    dna: RumourDNASchema,
    evidence: List[EvidenceRecordSchema],
    analysis_mode: str = "offline_fallback"
) -> ScoreBreakdownSchema:
    """
    FEATURE: HONEST CREDIBILITY SCORING & CONFIDENCE ENGINE
    Computes a transparent assessment based on verifiable signals:
    - Official Verdict: LIKELY TRUE, LIKELY FALSE, MIXED / PARTIALLY TRUE, UNVERIFIED
    - Confidence: HIGH, MEDIUM, LOW
    - Justified confidence percentage
    - Short verdict reason
    - Curated key excerpts
    Strictly upholds:
    - Contextual evidence alone produces an UNVERIFIED verdict and LOW confidence.
    - Duplicate search results do not count as multiple independent confirmations.
    - Source reliability remains separate from evidence relevance.
    """
    assertion = dna.factual_assertion or dna.normalized_text

    # Check for empty evidence
    if not evidence or len(evidence) == 0:
        return ScoreBreakdownSchema(
            source_reliability=0,
            direct_relevance=0,
            independent_corroboration=0,
            contradictory_penalty=0,
            recency=0,
            completeness=0,
            total_score=None,
            verdict="UNVERIFIED",
            confidence="LOW",
            confidence_score=None,
            verdict_reason="No verifiable evidence could be retrieved for this claim.",
            analysis_mode=analysis_mode,
            status_label="Not enough reliable evidence to assess this claim.",
            explanation="No verified public records, official circulars, or independent news reports could be retrieved for this statement.",
            key_excerpts=[]
        )

    # Detect if evidence is purely a generic fallback placeholder with no relevance
    if len(evidence) == 1 and "archive.factcheck.org" in evidence[0].url and evidence[0].reliability_score < 70:
        return ScoreBreakdownSchema(
            source_reliability=10,
            direct_relevance=5,
            independent_corroboration=0,
            contradictory_penalty=0,
            recency=5,
            completeness=5,
            total_score=None,
            verdict="UNVERIFIED",
            confidence="LOW",
            confidence_score=15,
            verdict_reason="Available archives contain no matching gazettes, official statements, or corroborating records for this claim.",
            analysis_mode=analysis_mode,
            status_label="Not enough reliable evidence to assess this claim.",
            explanation="Retrieved archives contain no matching gazettes, official statements, or corroborating reports for this claim.",
            key_excerpts=[]
        )

    supporting = [e for e in evidence if e.classification == "supporting"]
    contradictory = [e for e in evidence if e.classification == "contradictory"]
    contextual = [e for e in evidence if e.classification == "contextual"]
    irrelevant = [e for e in evidence if e.classification == "irrelevant"]
    
    # 1. Source Reliability (0 - 25 points)
    # Reflects the publisher authority tier independent of the claim outcome
    avg_rel = sum(e.reliability_score for e in evidence) / len(evidence)
    source_reliability_pts = int(round((avg_rel / 100.0) * 25))

    # 2. Direct Relevance (0 - 20 points)
    # Direct evidence (supporting or contradictory) provides relevant factual evaluation
    direct_records = len(supporting) + len(contradictory)
    if direct_records >= 2:
        direct_relevance_pts = 20
    elif direct_records == 1:
        direct_relevance_pts = 14
    else:
        direct_relevance_pts = 4

    # 3. Independent Corroboration (0 - 20 points)
    # Duplicate or substantially identical search results must NOT count as separate independent confirmations
    independent_supporting_publishers = []
    seen_excerpts = []
    
    for s in supporting:
        if not s.is_independent:
            continue
        pub = s.publisher.lower()
        # Check if excerpt is substantially identical (>60% token overlap) to previously counted corroboration
        is_substantially_identical = any(compute_text_similarity(s.excerpt, prev) >= 0.60 for prev in seen_excerpts)
        if pub not in independent_supporting_publishers and not is_substantially_identical:
            independent_supporting_publishers.append(pub)
            seen_excerpts.append(s.excerpt)

    if len(independent_supporting_publishers) >= 2:
        independent_pts = 20
    elif len(independent_supporting_publishers) == 1:
        independent_pts = 12
    else:
        independent_pts = 0

    # 4. Contradictory Penalty (0 to -45 points)
    contradictory_publishers = set(e.publisher.lower() for e in contradictory)
    if len(contradictory_publishers) >= 2:
        contradictory_penalty = -45
    elif len(contradictory_publishers) == 1:
        contradictory_penalty = -30
    else:
        contradictory_penalty = 0

    # 5. Recency (0 - 10 points)
    recency_pts = 9

    # 6. Verification Completeness (0 - 10 points)
    completeness_pts = 8 if direct_records >= 2 else (5 if direct_records == 1 else 3)

    # 7. Verdict, Confidence, and Reason Determination:
    # Insufficient Direct Evidence Rule:
    # If there is neither supporting nor contradictory evidence (only contextual or irrelevant),
    # verdict MUST be UNVERIFIED and total_score MUST be None.
    if not supporting and not contradictory:
        verdict = "UNVERIFIED"
        confidence = "LOW"
        confidence_score = 15
        total_score = None
        verdict_reason = f"Available records provide general background on the subject but do not contain verifiable evidence to confirm or refute '{assertion[:60]}'."
        status_label = "Not enough reliable evidence to assess this claim."
        key_excerpts = select_key_excerpts(evidence, verdict)
        explanation = f"Retrieved {len(contextual)} background records discussing the general subject, but none directly confirm or refute the specific assertion."
        
        return ScoreBreakdownSchema(
            source_reliability=source_reliability_pts,
            direct_relevance=direct_relevance_pts,
            independent_corroboration=0,
            contradictory_penalty=0,
            recency=recency_pts,
            completeness=completeness_pts,
            total_score=None,
            verdict=verdict,
            confidence=confidence,
            confidence_score=confidence_score,
            verdict_reason=verdict_reason,
            analysis_mode=analysis_mode,
            status_label=status_label,
            explanation=explanation,
            key_excerpts=key_excerpts
        )

    # Contradicted by evidence -> LIKELY FALSE
    if contradictory and not supporting:
        raw_score = max(5, source_reliability_pts + direct_relevance_pts + contradictory_penalty)
        total_score = min(35, max(5, int(round(raw_score))))
        verdict = "LIKELY FALSE"
        status_label = "Directly Contradicted by Trusted Sources"

        # Confidence based on authority and publisher count
        high_rel_contradiction = any(e.reliability_score >= 85 for e in contradictory)
        if len(contradictory_publishers) >= 2 or high_rel_contradiction:
            confidence = "HIGH"
            confidence_score = 90
        else:
            confidence = "MEDIUM"
            confidence_score = 70

        first_contra = contradictory[0]
        verdict_reason = f"Verified records from {first_contra.publisher} directly contradict this claim ({first_contra.relevance_reason.rstrip('.')})."

    # Mixed / Conflicting evidence -> MIXED / PARTIALLY TRUE
    elif contradictory and supporting:
        raw_score = 45 + (len(supporting) - len(contradictory)) * 8
        total_score = max(25, min(65, int(round(raw_score))))
        verdict = "MIXED / PARTIALLY TRUE"
        status_label = "Conflicting Evidence Identified"
        confidence = "MEDIUM"
        confidence_score = 65
        verdict_reason = f"Retrieved evidence contains both supporting reports ({len(supporting)}) and contradictory records ({len(contradictory)}), indicating partial accuracy or disputed facts."

    # Supported by evidence -> LIKELY TRUE
    else:
        raw_score = source_reliability_pts + direct_relevance_pts + independent_pts + recency_pts + completeness_pts
        total_score = min(98, max(65, int(round(raw_score))))
        verdict = "LIKELY TRUE"
        status_label = "Corroborated by Verified Evidence"

        if len(independent_supporting_publishers) >= 2 and source_reliability_pts >= 16:
            confidence = "HIGH"
            confidence_score = min(95, 75 + len(independent_supporting_publishers) * 5)
        elif len(independent_supporting_publishers) >= 1 and source_reliability_pts >= 14:
            confidence = "MEDIUM"
            confidence_score = 75
        else:
            confidence = "LOW"
            confidence_score = 50

        first_supp = supporting[0]
        verdict_reason = f"Verified records from {first_supp.publisher} directly corroborate this factual assertion with no unresolved contradictory evidence."

    key_excerpts = select_key_excerpts(evidence, verdict)

    explanation = (
        f"Assessed {len(evidence)} evidence sources. "
        f"Found {len(supporting)} supporting, {len(contradictory)} contradictory, {len(contextual)} contextual, and {len(irrelevant)} irrelevant items. "
        f"Source reliability rated {source_reliability_pts}/25, with {len(independent_supporting_publishers)} independent corroborating publisher(s)."
    )

    return ScoreBreakdownSchema(
        source_reliability=source_reliability_pts,
        direct_relevance=direct_relevance_pts,
        independent_corroboration=independent_pts,
        contradictory_penalty=contradictory_penalty,
        recency=recency_pts,
        completeness=completeness_pts,
        total_score=total_score,
        verdict=verdict,
        confidence=confidence,
        confidence_score=confidence_score,
        verdict_reason=verdict_reason,
        analysis_mode=analysis_mode,
        status_label=status_label,
        explanation=explanation,
        key_excerpts=key_excerpts
    )
