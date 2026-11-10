import pytest
from backend.app.schemas.claim import EvidenceRecordSchema, RumourDNASchema
from backend.app.services.credibility_scoring import calculate_evidence_score
from backend.app.services.claim_extraction import extract_rumour_dna

def test_scoring_insufficient_evidence():
    dna = extract_rumour_dna("Some unverified rumor with no records")
    breakdown = calculate_evidence_score(dna, [])
    assert breakdown.total_score is None
    assert breakdown.verdict in ("UNVERIFIED", "Unverified")
    assert "Not enough reliable evidence" in breakdown.status_label

def test_scoring_contradictory_evidence():
    dna = extract_rumour_dna("All schools in the state are shut down indefinitely")
    evidence = [
        EvidenceRecordSchema(
            url="https://gov.education.org",
            publisher="Ministry of Education",
            title="Clarification on School Functioning",
            publication_date="2026-03-12",
            retrieval_date="2026-03-14",
            excerpt="No statewide closure has been declared. All institutions remain open.",
            classification="contradictory",
            relevance_reason="Refutes shutdown",
            reliability_score=95,
            is_independent=True
        ),
        EvidenceRecordSchema(
            url="https://news.org",
            publisher="News Agency",
            title="State refutes rumor",
            publication_date="2026-03-13",
            retrieval_date="2026-03-14",
            excerpt="Officials confirm all institutions function normally.",
            classification="contradictory",
            relevance_reason="Independent confirmation",
            reliability_score=90,
            is_independent=True
        )
    ]
    breakdown = calculate_evidence_score(dna, evidence)
    assert breakdown.total_score is not None
    assert breakdown.total_score <= 30
    assert breakdown.verdict in ("LIKELY FALSE", "Contradicted", "Mostly contradicted")
    assert breakdown.contradictory_penalty < 0
