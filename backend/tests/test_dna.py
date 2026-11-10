import pytest
from backend.app.services.claim_extraction import extract_rumour_dna, extract_scope
from backend.app.services.entity_extraction import extract_entities

def test_extract_dna_single_school():
    claim = "Oakridge High School will remain closed for two days for preventive pest fumigation."
    dna = extract_rumour_dna(claim)
    assert dna.scope == "specific"
    assert "pest fumigation" in dna.normalized_text
    assert dna.semantic_hash is not None
    assert len(dna.semantic_hash) == 16
    assert any(e.name.lower() == "two days" for e in dna.entities)

def test_extract_dna_statewide_escalation():
    claim = "State Government has declared holidays for all educational institutions statewide."
    dna = extract_rumour_dna(claim)
    assert dna.scope == "statewide"
    assert "holidays" in dna.factual_assertion.lower() or "state" in dna.factual_assertion.lower()

def test_extract_entities_quantities_and_dates():
    text = "The Ministry allocated $5,000 relief grant to 1,200 families on January 15."
    entities = extract_entities(text)
    categories = [e.category for e in entities]
    assert "date" in categories
    assert "quantity" in categories
