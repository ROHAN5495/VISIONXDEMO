"""
Automated Test Suite for Verdict, Confidence, Evidence Classification & AI Integration
Covers all 12 backend scenarios specified in Section 7:
1. A claim supported by relevant evidence.
2. A claim contradicted by relevant evidence.
3. A claim with both supporting and contradicting evidence.
4. An unrelated source.
5. Negated claims.
6. Reversed facts such as east versus west.
7. Duplicate sources.
8. Insufficient evidence.
9. Missing Gemini API key.
10. Gemini quota or network failure.
11. Invalid AI response.
12. Correct offline fallback.
"""
import pytest
from unittest.mock import patch, MagicMock
import httpx
from backend.app.schemas.claim import EvidenceRecordSchema, InvestigationCreateRequest
from backend.app.services.claim_extraction import extract_rumour_dna
from backend.app.services.contradiction_detection import assess_contradictions, classify_single_record
from backend.app.services.credibility_scoring import calculate_evidence_score
from backend.app.services.ai_service import GeminiAIService
from backend.app.routers.investigations import create_investigation
from backend.app.database import init_db, SessionLocal

@pytest.fixture(scope="module")
def db_session():
    init_db()
    db = SessionLocal()
    yield db
    db.close()


# ==============================================================================
# SCENARIO 1: Claim supported by relevant evidence
# ==============================================================================
def test_scenario_1_supported_claim():
    claim_text = "The Sun rises in the east."
    dna = extract_rumour_dna(claim_text)
    evidence = [
        EvidenceRecordSchema(
            url="https://science.nasa.gov/sun",
            publisher="NASA Science",
            title="Solar Motion",
            retrieval_date="2026-03-01",
            excerpt="The Sun appears to rise in the east because Earth rotates on its axis eastward.",
            classification="contextual",
            relevance_reason="Solar motion",
            reliability_score=95,
            is_independent=True
        ),
        EvidenceRecordSchema(
            url="https://britannica.com/sunrise",
            publisher="Encyclopaedia Britannica",
            title="Sunrise Mechanics",
            retrieval_date="2026-03-01",
            excerpt="The Sun rises on the eastern horizon each morning due to Earth rotating eastward on its axis.",
            classification="contextual",
            relevance_reason="Sunrise definition",
            reliability_score=92,
            is_independent=True
        )
    ]
    assessed = assess_contradictions(dna, evidence)
    assert all(e.classification == "supporting" for e in assessed)
    
    score = calculate_evidence_score(dna, assessed)
    assert score.verdict == "LIKELY TRUE"
    assert score.confidence == "HIGH"
    assert score.confidence_score is not None and score.confidence_score >= 80
    assert len(score.key_excerpts) >= 1
    assert score.key_excerpts[0]["is_snippet"] is True


# ==============================================================================
# SCENARIO 2: Claim contradicted by relevant evidence
# ==============================================================================
def test_scenario_2_contradicted_claim():
    claim_text = "All schools in the state are closed indefinitely due to emergencies."
    dna = extract_rumour_dna(claim_text)
    evidence = [
        EvidenceRecordSchema(
            url="https://education.gov/press-release",
            publisher="Ministry of Education",
            title="Official Statement Regarding Operational Schools",
            retrieval_date="2026-03-14",
            excerpt="No statewide closure has been declared. All educational institutions remain open and fully functional.",
            classification="contextual",
            relevance_reason="Refutation",
            reliability_score=96,
            is_independent=True
        )
    ]
    assessed = assess_contradictions(dna, evidence)
    assert assessed[0].classification == "contradictory"

    score = calculate_evidence_score(dna, assessed)
    assert score.verdict == "LIKELY FALSE"
    assert score.confidence == "HIGH"
    assert "directly contradict" in score.verdict_reason.lower()


# ==============================================================================
# SCENARIO 3: Claim with both supporting and contradicting evidence (Mixed / Partially True)
# ==============================================================================
def test_scenario_3_mixed_evidence():
    claim_text = "Compound TX-94 is a cure for cancer."
    dna = extract_rumour_dna(claim_text)
    evidence = [
        EvidenceRecordSchema(
            url="https://biotech-trials.org/tx94-phase1",
            publisher="Biotech Clinical Registry",
            title="Phase 1 Tolerability of Compound TX-94",
            retrieval_date="2026-03-01",
            excerpt="Laboratory trials report Compound TX-94 cured cancer tumors in 85% of animal subjects.",
            classification="supporting",
            relevance_reason="Confirms active research",
            reliability_score=85,
            is_independent=True
        ),
        EvidenceRecordSchema(
            url="https://fda.gov/warnings/unapproved-claims",
            publisher="Food and Drug Administration (FDA)",
            title="Advisory on Unapproved Cancer Claims",
            retrieval_date="2026-03-01",
            excerpt="Compound TX-94 is NOT an approved cancer cure and clinical efficacy has not been demonstrated.",
            classification="contradictory",
            relevance_reason="Refutes cure claims",
            reliability_score=98,
            is_independent=True
        )
    ]
    assessed = assess_contradictions(dna, evidence)
    score = calculate_evidence_score(dna, assessed)
    assert score.verdict == "MIXED / PARTIALLY TRUE"
    assert score.confidence == "MEDIUM"
    assert "both supporting" in score.verdict_reason.lower()


# ==============================================================================
# SCENARIO 4: Unrelated / Irrelevant source
# ==============================================================================
def test_scenario_4_unrelated_source():
    claim_text = "The Sun rises in the east."
    dna = extract_rumour_dna(claim_text)
    rec = EvidenceRecordSchema(
        url="https://market-news.com/tech-stocks",
        publisher="Market Today",
        title="Tech stocks rally after earnings reports",
        retrieval_date="2026-03-01",
        excerpt="Semiconductor shares surged 4.2% following quarterly earnings updates and revenue projections.",
        classification="contextual",
        relevance_reason="Off topic",
        reliability_score=80,
        is_independent=True
    )
    classification, reason = classify_single_record(dna, rec)
    assert classification == "irrelevant"
    assert "unrelated source" in reason.lower()


# ==============================================================================
# SCENARIO 5: Negated claim with affirmative evidence
# ==============================================================================
def test_scenario_5_negated_claim():
    claim_text = "The Sun does not rise in the east."
    dna = extract_rumour_dna(claim_text)
    assert dna.is_negated is True
    
    evidence = [
        EvidenceRecordSchema(
            url="https://science.nasa.gov",
            publisher="NASA",
            title="Earth Rotation",
            retrieval_date="2026-03-01",
            excerpt="The Sun appears to rise in the east because Earth rotates on its axis.",
            classification="contextual",
            relevance_reason="Solar motion",
            reliability_score=95,
            is_independent=True
        )
    ]
    assessed = assess_contradictions(dna, evidence)
    # Evidence affirms rising in the east, which directly contradicts the negative claim
    assert assessed[0].classification == "contradictory"
    score = calculate_evidence_score(dna, assessed)
    assert score.verdict == "LIKELY FALSE"


# ==============================================================================
# SCENARIO 6: Reversed facts (East versus West)
# ==============================================================================
def test_scenario_6_reversed_facts_east_vs_west():
    # THE ORIGINAL REPORTED BUG: "The Sun rises in the west."
    claim_text = "The Sun rises in the west."
    dna = extract_rumour_dna(claim_text)
    evidence = [
        EvidenceRecordSchema(
            url="https://starchild.gsfc.nasa.gov",
            publisher="NASA Starchild",
            title="Why does the Sun rise in the east and set in the west?",
            retrieval_date="2026-03-01",
            excerpt="The Sun, the Moon, the planets, and the stars all rise in the east and set in the west because Earth rotates eastward.",
            classification="contextual",
            relevance_reason="Solar dynamics",
            reliability_score=94,
            is_independent=True
        )
    ]
    assessed = assess_contradictions(dna, evidence)
    # Must be CONTRADICTORY, never supporting!
    assert assessed[0].classification == "contradictory"
    
    score = calculate_evidence_score(dna, assessed)
    assert score.verdict == "LIKELY FALSE"
    assert score.confidence == "HIGH"
    assert score.total_score is not None and score.total_score <= 35


# ==============================================================================
# SCENARIO 7: Duplicate sources do not double-count independent corroboration
# ==============================================================================
def test_scenario_7_duplicate_sources_deduplication():
    claim_text = "The Sun rises in the east."
    dna = extract_rumour_dna(claim_text)
    
    shared_excerpt = "The Sun appears to rise in the east and set in the west because Earth rotates on its axis."
    evidence = [
        EvidenceRecordSchema(
            url="https://wire-news-a.com/sunrise",
            publisher="Wire Outlet A",
            title="Sunrise Mechanics",
            retrieval_date="2026-03-01",
            excerpt=shared_excerpt,
            classification="supporting",
            relevance_reason="Direct alignment",
            reliability_score=85,
            is_independent=True
        ),
        EvidenceRecordSchema(
            url="https://syndicate-mirror-b.com/reprint-sunrise",
            publisher="Syndicate Mirror B",
            title="Sunrise Mechanics (Reprint)",
            retrieval_date="2026-03-01",
            excerpt=shared_excerpt,  # Identical syndicated excerpt
            classification="supporting",
            relevance_reason="Syndicated mirror",
            reliability_score=80,
            is_independent=True
        )
    ]
    score = calculate_evidence_score(dna, evidence)
    # Only 1 unique independent corroborating cluster must be credited (12 pts, not 20 pts)
    assert score.independent_corroboration == 12
    assert "with 1 independent corroborating publisher(s)" in score.explanation


# ==============================================================================
# SCENARIO 8: Insufficient evidence produces UNVERIFIED and LOW confidence
# ==============================================================================
def test_scenario_8_insufficient_evidence():
    claim_text = "The Sun rises in the east."
    dna = extract_rumour_dna(claim_text)
    
    # Only topical background that does not address sunrise direction
    evidence = [
        EvidenceRecordSchema(
            url="https://astro-facts.com/solar-core",
            publisher="Astro Facts",
            title="Solar Fusion",
            retrieval_date="2026-03-01",
            excerpt="The core of the Sun extends from the center to about 20-25% of the solar radius.",
            classification="contextual",
            relevance_reason="Solar core physics",
            reliability_score=85,
            is_independent=True
        )
    ]
    assessed = assess_contradictions(dna, evidence)
    assert assessed[0].classification == "contextual"

    score = calculate_evidence_score(dna, assessed)
    assert score.verdict == "UNVERIFIED"
    assert score.confidence == "LOW"
    assert score.total_score is None


# ==============================================================================
# SCENARIO 9: Missing Gemini API key -> Graceful fallback
# ==============================================================================
def test_scenario_9_missing_gemini_api_key():
    service = GeminiAIService(api_key="")
    assert service.is_available() is False
    
    dna = extract_rumour_dna("The Sun rises in the east.")
    data, success, msg = service.analyze_evidence(dna, [])
    assert success is False
    assert data is None
    assert "inactive" in msg.lower() or "not configured" in msg.lower()


# ==============================================================================
# SCENARIO 10: Gemini quota (HTTP 429) or network failure handling
# ==============================================================================
def test_scenario_10_gemini_quota_or_network_failure():
    service = GeminiAIService(api_key="valid-test-key")
    
    mock_resp = MagicMock()
    mock_resp.status_code = 429
    mock_resp.text = "Quota exceeded for quota group default"
    
    mock_client = MagicMock()
    mock_client.post.return_value = mock_resp
    mock_client.__enter__.return_value = mock_client
    mock_client.__exit__.return_value = None
    
    with patch("backend.app.services.ai_service.httpx.Client", return_value=mock_client):
        dna = extract_rumour_dna("The Sun rises in the east.")
        rec = EvidenceRecordSchema(
            url="https://nasa.gov",
            publisher="NASA",
            title="Sunrise",
            retrieval_date="2026-03-01",
            excerpt="The Sun rises in the east.",
            classification="contextual",
            relevance_reason="test",
            reliability_score=90
        )
        data, success, msg = service.analyze_evidence(dna, [rec])
        assert success is False
        assert data is None
        assert "quota" in msg.lower() or "rate limit" in msg.lower()


# ==============================================================================
# SCENARIO 11: Invalid AI response handling
# ==============================================================================
def test_scenario_11_invalid_ai_response():
    service = GeminiAIService(api_key="valid-test-key")
    
    # Mock AI returning non-JSON or invalid schema
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "candidates": [
            {
                "content": {
                    "parts": [{"text": "Not a JSON structure at all"}]
                }
            }
        ]
    }
    
    mock_client = MagicMock()
    mock_client.post.return_value = mock_resp
    mock_client.__enter__.return_value = mock_client
    mock_client.__exit__.return_value = None
    
    with patch("backend.app.services.ai_service.httpx.Client", return_value=mock_client):
        dna = extract_rumour_dna("The Sun rises in the east.")
        rec = EvidenceRecordSchema(
            url="https://nasa.gov",
            publisher="NASA",
            title="Sunrise",
            retrieval_date="2026-03-01",
            excerpt="The Sun rises in the east.",
            classification="contextual",
            relevance_reason="test",
            reliability_score=90
        )
        data, success, msg = service.analyze_evidence(dna, [rec])
        assert success is False
        assert data is None
        assert "invalid json" in msg.lower()


# ==============================================================================
# SCENARIO 12: Correct offline fallback when live search is unavailable
# ==============================================================================
def test_scenario_12_correct_offline_fallback(db_session):
    with patch("backend.app.services.evidence_search.settings.TAVILY_API_KEY", ""):
        req = InvestigationCreateRequest(
            claim_text="Oakridge High School will remain closed for two days for pest control.",
            source_origin="Parent Notice",
            origin_type="user_submitted",
            recorded_date="2026-03-15",
            is_demo=False
        )
        inv = create_investigation(req, db_session)
        assert inv.is_demo is True
        assert inv.evidence_mode == "offline_demo"
        assert inv.analysis_mode == "offline_fallback"
        assert all(e.is_demo is True for e in inv.evidence)
