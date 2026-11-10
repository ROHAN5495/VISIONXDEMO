import pytest
from backend.app.services.mutation_analysis import analyze_mutations
from backend.app.services.claim_extraction import extract_rumour_dna

def test_mutation_scope_expansion_and_conditions_removed():
    v1 = "Oakridge High School will remain closed for two days for routine preventive pest fumigation."
    v2 = "All schools in the district are closed until further notice due to severe chemical health hazards."
    
    dna1 = extract_rumour_dna(v1)
    dna2 = extract_rumour_dna(v2)
    report = analyze_mutations(v1, v2, dna1, dna2)
    
    assert report.has_mutation is True
    assert report.scope_change["direction"] == "expanded"
    # Scope went from specific to district
    assert report.scope_change["from"] == "specific"
    assert report.scope_change["to"] == "district"
    # Condition words like fumigation were dropped
    assert "fumigation" in report.missing_conditions
    # Escalating words like 'all' added
    assert any(term in report.unsupported_additions for term in ["all", "hazard"]) or len(report.added_information) > 0
    # Human explanation is generated
    assert len(report.explanation) > 10
    # Check diff token types present
    token_types = {t.type for t in report.diff_tokens}
    assert "equal" in token_types
    assert ("added" in token_types or "misleading" in token_types or "context" in token_types)

def test_mutation_unaltered_identical():
    text = "The committee will convene on Friday afternoon."
    report = analyze_mutations(text, text)
    assert report.has_mutation is False
    assert report.scope_change["direction"] == "unchanged"
