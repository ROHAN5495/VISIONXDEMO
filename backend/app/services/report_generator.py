from typing import List, Optional
from backend.app.schemas.claim import (
    RumourDNASchema,
    EvidenceRecordSchema,
    MutationReportSchema,
    ScoreBreakdownSchema
)

def generate_human_explanation(
    dna: RumourDNASchema,
    evidence: List[EvidenceRecordSchema],
    score_breakdown: ScoreBreakdownSchema,
    mutation_report: Optional[MutationReportSchema] = None
) -> str:
    """
    FEATURE D — HUMAN TRUTH EXPLANATION
    Produces natural, concise, evidence-first explanations.
    Adheres strictly to the writing rules:
    - Short, natural sentences.
    - Evidence stated before conclusions.
    - Honest admission of uncertainty.
    - Zero AI jargon.
    """
    supporting = [e for e in evidence if e.classification == "supporting"]
    contradictory = [e for e in evidence if e.classification == "contradictory"]
    contextual = [e for e in evidence if e.classification == "contextual"]
    
    sentences: List[str] = []

    # 1. State the evidence facts first
    if contradictory:
        top_contra = contradictory[0]
        sentences.append(
            f"Official statements from {top_contra.publisher} clarify that '{top_contra.excerpt}'."
        )
        if len(contradictory) > 1:
            second_contra = contradictory[1]
            sentences.append(
                f"This is also confirmed by {second_contra.publisher}, which found no record matching the broader claim."
            )
    elif supporting:
        top_supp = supporting[0]
        sentences.append(
            f"Records from {top_supp.publisher} indicate that '{top_supp.excerpt}'."
        )
    elif contextual:
        top_context = contextual[0]
        sentences.append(
            f"Available background from {top_context.publisher} discusses related developments, but does not confirm this specific message."
        )
    else:
        sentences.append(
            "We checked public records, official circulars, and verified reports, but found no direct documentation."
        )

    # 2. Address the mutation or scope if there was a previous version
    if mutation_report and mutation_report.has_mutation:
        if mutation_report.scope_change.get("direction") == "expanded":
            from_scope = mutation_report.scope_change.get("from", "a specific site")
            to_scope = mutation_report.scope_change.get("to", "a wider area")
            sentences.append(
                f"Notice how the text changed: an earlier version discussed {from_scope}, but this version claims it applies to {to_scope}."
            )
        if mutation_report.missing_conditions:
            conds = ", ".join(mutation_report.missing_conditions)
            sentences.append(
                f"Important qualifiers were dropped ({conds}), which distorts what actually happened."
            )
        if mutation_report.changed_numbers:
            sentences.append(
                "Key numbers were also altered between forwards."
            )

    # 3. Honest conclusion and practical advice (VERIFY BEFORE YOU SHARE)
    if contradictory:
        sentences.append(
            "Because reliable sources refute the wider statement, sharing this forward as confirmed news spreads misleading information."
        )
    elif supporting:
        sentences.append(
            "The statement matches documented events for the stated location and timeframe."
        )
    elif score_breakdown.verdict == "Unverified":
        sentences.append(
            "Without reliable primary sources, this claim cannot be confirmed. Please verify with official channels before forwarding."
        )
    else:
        sentences.append(
            "Portions of the report contain truthful background, but key details remain unverified or exaggerated."
        )

    return " ".join(sentences)
