"""
Automated Test Suite for Evidence Classification and Verdict Engine
Section 8 compliance tests: Tests 1 through 8
"""
import pytest
from unittest.mock import patch, MagicMock
from backend.app.schemas.claim import EvidenceRecordSchema, InvestigationCreateRequest
from backend.app.services.claim_extraction import extract_rumour_dna
from backend.app.services.contradiction_detection import assess_contradictions
from backend.app.services.credibility_scoring import calculate_evidence_score
from backend.app.routers.investigations import create_investigation
from backend.app.database import init_db, SessionLocal

@pytest.fixture(scope="module")
def db_session():
    init_db()
    db = SessionLocal()
    yield db
    db.close()


# ==============================================================================
# TEST 1: Sun rises in the east -> Supporting Evidence
# ==============================================================================
def test_1_sun_rises_in_east_supporting():
    claim_text = "The Sun rises in the east."
    dna = extract_rumour_dna(claim_text)
    
    evidence = [
        EvidenceRecordSchema(
            url="https://science.nasa.gov/solar-system/sun",
            publisher="NASA Science",
            title="Solar Motion and Earth Rotation",
            publication_date="2026-01-15",
            retrieval_date="2026-03-01",
            excerpt="The Sun appears to rise in the east because Earth rotates on its axis towards the east.",
            classification="contextual",  # re-assessed by contradiction detection
            relevance_reason="Explains apparent motion of the Sun",
            reliability_score=95,
            is_independent=True
        )
    ]
    
    reassessed = assess_contradictions(dna, evidence)
    assert reassessed[0].classification == "supporting"
    assert "corroborates" in reassessed[0].relevance_reason.lower() or "confirms" in reassessed[0].relevance_reason.lower()


# ==============================================================================
# TEST 2: Contextual solar fact -> Contextual Evidence
# ==============================================================================
def test_2_sun_contextual_solar_fact():
    claim_text = "The Sun rises in the east."
    dna = extract_rumour_dna(claim_text)
    
    evidence = [
        EvidenceRecordSchema(
            url="https://spacefacts.org/the-sun",
            publisher="Space Facts",
            title="The Solar Core and Mass",
            publication_date="2025-11-20",
            retrieval_date="2026-03-01",
            excerpt="The Sun is the star at the centre of our solar system and accounts for 99.8% of the system's mass.",
            classification="contextual",
            relevance_reason="Solar overview",
            reliability_score=85,
            is_independent=True
        )
    ]
    
    reassessed = assess_contradictions(dna, evidence)
    assert reassessed[0].classification == "contextual"
    assert "does not confirm or refute" in reassessed[0].relevance_reason.lower() or "background" in reassessed[0].relevance_reason.lower()


# ==============================================================================
# TEST 3: Contradictory solar claim -> Contradictory Evidence
# ==============================================================================
def test_3_sun_contradictory_evidence():
    claim_text = "The Sun rises in the east."
    dna = extract_rumour_dna(claim_text)
    
    evidence = [
        EvidenceRecordSchema(
            url="https://astro-journal.org/erroneous-claims",
            publisher="Astronomical Review",
            title="Directional Analysis",
            publication_date="2026-02-10",
            retrieval_date="2026-03-01",
            excerpt="Astronomical measurements establish that the Sun normally rises in the west, contradicting standard assumptions.",
            classification="contextual",
            relevance_reason="Direction of sunrise",
            reliability_score=90,
            is_independent=True
        )
    ]
    
    reassessed = assess_contradictions(dna, evidence)
    assert reassessed[0].classification == "contradictory"
    assert "contradicts" in reassessed[0].relevance_reason.lower() or "opposing" in reassessed[0].relevance_reason.lower()


# ==============================================================================
# TEST 4: Negated claim with standard evidence -> Contradictory Evidence
# ==============================================================================
def test_4_negated_claim_with_standard_evidence():
    claim_text = "The Sun does not rise in the east."
    dna = extract_rumour_dna(claim_text)
    assert dna.is_negated is True
    
    evidence = [
        EvidenceRecordSchema(
            url="https://nasa.gov/sun",
            publisher="NASA",
            title="Earth Rotation and Sunrise",
            publication_date="2026-01-10",
            retrieval_date="2026-03-01",
            excerpt="The Sun appears to rise in the east because Earth rotates towards the east.",
            classification="contextual",
            relevance_reason="Solar motion",
            reliability_score=95,
            is_independent=True
        )
    ]
    
    reassessed = assess_contradictions(dna, evidence)
    # The evidence affirms that the Sun rises in the east, directly refuting the negative claim
    assert reassessed[0].classification == "contradictory"
    assert "contradicts" in reassessed[0].relevance_reason.lower()


# ==============================================================================
# TEST 5: Duplicate evidence snippets deduplication
# ==============================================================================
def test_5_duplicate_evidence_snippets_deduplication():
    claim_text = "The Sun rises in the east."
    dna = extract_rumour_dna(claim_text)
    
    identical_excerpt = "The Sun appears to rise in the east because Earth rotates on its axis from west to east."
    
    duplicate_evidence = [
        EvidenceRecordSchema(
            url="https://source-a.org/sun-east",
            publisher="Science Wire A",
            title="Sun rises in east",
            publication_date="2026-02-01",
            retrieval_date="2026-03-01",
            excerpt=identical_excerpt,
            classification="supporting",
            relevance_reason="Direct alignment",
            reliability_score=90,
            is_independent=True
        ),
        EvidenceRecordSchema(
            url="https://syndicated-b.net/reprint-sun",
            publisher="Syndicate Mirror B",
            title="Sun rises in east (syndicated reprint)",
            publication_date="2026-02-02",
            retrieval_date="2026-03-01",
            excerpt=identical_excerpt,  # Substantially identical text
            classification="supporting",
            relevance_reason="Syndicated copy",
            reliability_score=85,
            is_independent=True
        )
    ]
    
    breakdown_dup = calculate_evidence_score(dna, duplicate_evidence)
    
    # When snippets are identical, only 1 independent confirmation must be scored
    assert breakdown_dup.independent_corroboration == 12
    assert "with 1 independent corroborating publisher(s)" in breakdown_dup.explanation
    
    # In contrast, two distinct excerpts from two distinct publishers receive full corroboration (20 pts)
    distinct_evidence = [
        duplicate_evidence[0],
        EvidenceRecordSchema(
            url="https://astronomy-today.edu/celestial-mechanics",
            publisher="University Observatory",
            title="Earth Rotation Principles",
            publication_date="2026-02-03",
            retrieval_date="2026-03-01",
            excerpt="Because of our planet's prograde rotation, morning light first illuminates the eastern horizon every day.",
            classification="supporting",
            relevance_reason="Independent celestial physics source",
            reliability_score=95,
            is_independent=True
        )
    ]
    breakdown_distinct = calculate_evidence_score(dna, distinct_evidence)
    assert breakdown_distinct.independent_corroboration == 20
    assert "with 2 independent corroborating publisher(s)" in breakdown_distinct.explanation


# ==============================================================================
# TEST 6: Contextual evidence only -> Unverified verdict and total_score is None
# ==============================================================================
def test_6_contextual_evidence_only_unverified():
    claim_text = "The Sun rises in the east."
    dna = extract_rumour_dna(claim_text)
    
    evidence = [
        EvidenceRecordSchema(
            url="https://astro-facts.com/sun-1",
            publisher="Astronomy Facts",
            title="Solar Corona Properties",
            publication_date="2025-10-10",
            retrieval_date="2026-03-01",
            excerpt="The Sun's corona is an aura of plasma that surrounds the Sun and other celestial bodies.",
            classification="contextual",
            relevance_reason="Contextual solar physics",
            reliability_score=88,
            is_independent=True
        ),
        EvidenceRecordSchema(
            url="https://astro-facts.com/sun-2",
            publisher="Solar Physics Daily",
            title="Sunspots and Magnetic Cycles",
            publication_date="2025-11-12",
            retrieval_date="2026-03-01",
            excerpt="Sunspots are temporary phenomena on the Sun's photosphere that appear as spots darker than the surrounding areas.",
            classification="contextual",
            relevance_reason="Solar physics",
            reliability_score=82,
            is_independent=True
        )
    ]
    
    breakdown = calculate_evidence_score(dna, evidence)
    
    # Must produce UNVERIFIED verdict and None score
    assert breakdown.verdict in ("UNVERIFIED", "Unverified")
    assert breakdown.total_score is None
    assert "not enough reliable evidence" in breakdown.status_label.lower()
    assert "none directly confirm or refute" in breakdown.explanation.lower()


# ==============================================================================
# TEST 7: Offline fallback mode -> is_demo=True, evidence_mode="offline_demo"
# ==============================================================================
def test_7_offline_fallback_mode(db_session):
    # When TAVILY_API_KEY is empty, search_live_evidence must fall back to offline demo records
    with patch("backend.app.services.evidence_search.settings.TAVILY_API_KEY", ""):
        req = InvestigationCreateRequest(
            claim_text="Oakridge High School will remain closed for two days for pest control.",
            source_origin="Parent Chat",
            origin_type="user_submitted",
            recorded_date="2026-03-15",
            is_demo=False  # User requested live, but system must fall back honestly to offline demo
        )
        inv = create_investigation(req, db_session)
        
        # Must be marked as demo/offline fallback, not falsely claiming to be live
        assert inv.is_demo is True
        assert inv.evidence_mode == "offline_demo"
        assert len(inv.evidence) > 0
        for ev in inv.evidence:
            assert ev.is_demo is True


# ==============================================================================
# TEST 8: Live search mode -> is_demo=False, evidence_mode="live"
# ==============================================================================
def test_8_live_search_mode_mocked(db_session):
    # Mock httpx response from Tavily returning live evidence
    mock_tavily_payload = {
        "results": [
            {
                "url": "https://www.nasa.gov/sun-east-rising",
                "title": "Why the Sun Appears to Rise in the East",
                "content": "The Sun appears to rise in the east and set in the west because Earth rotates eastward on its axis.",
                "published_date": "2026-01-20"
            },
            {
                "url": "https://www.britannica.com/science/sunrise",
                "title": "Sunrise Definition and Celestial Mechanics",
                "content": "Sunrise is the moment when the upper rim of the Sun appears on the eastern horizon due to planetary rotation.",
                "published_date": "2025-12-10"
            }
        ]
    }
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_tavily_payload
    
    mock_client = MagicMock()
    mock_client.post.return_value = mock_response
    mock_client.__enter__.return_value = mock_client
    mock_client.__exit__.return_value = None
    
    with patch("backend.app.services.evidence_search.settings.TAVILY_API_KEY", "tvly-valid-mock-key"), \
         patch("backend.app.services.evidence_search.httpx.Client", return_value=mock_client):
        
        req = InvestigationCreateRequest(
            claim_text="The Sun rises in the east.",
            source_origin="Science Query",
            origin_type="observed",
            recorded_date="2026-03-15",
            is_demo=False
        )
        inv = create_investigation(req, db_session)
        
        # Verify investigation status and badges
        assert inv.is_demo is False
        assert inv.evidence_mode == "live"
        assert len(inv.evidence) >= 2
        
        # Verify all evidence items are marked as live (is_demo=False)
        for ev in inv.evidence:
            assert ev.is_demo is False
        
        # Verify evidence classification is supporting
        supporting_records = [ev for ev in inv.evidence if ev.classification == "supporting"]
        assert len(supporting_records) >= 1, "Live snippets confirming sunrise in east must be classified as supporting"
        
        # Verdict must be Supported, Mostly supported, or LIKELY TRUE
        assert inv.verdict in ("LIKELY TRUE", "Supported", "Mostly supported")
        assert inv.score is not None
        assert inv.score >= 50
