import difflib
import re
from typing import Dict, Any, List, Tuple
from backend.app.schemas.claim import (
    RumourDNASchema,
    MutationReportSchema,
    MutationDiffToken
)
from backend.app.services.claim_extraction import extract_rumour_dna

SCOPE_RANK = {
    "specific": 1,
    "local": 2,
    "district": 3,
    "statewide": 4,
    "national": 5,
    "global": 6,
    "general": 2
}

CONDITION_WORDS = {
    "if", "only", "unless", "subject to", "pending", "phase 1", "preliminary",
    "temporary", "tentative", "proposed", "draft", "condition", "provided",
    "eligible", "restricted", "fumigation", "maintenance", "sanitization"
}

MISLEADING_ESCALATIONS = {
    "all", "every", "entire", "indefinite", "forever", "banned", "permanently",
    "emergency", "declared", "secretly", "leaked", "coverup", "deadly",
    "miracle", "cure", "100%", "guaranteed", "confirmed", "breaking"
}

def analyze_mutations(text1: str, text2: str, dna1: RumourDNASchema = None, dna2: RumourDNASchema = None) -> MutationReportSchema:
    """
    FEATURE B — MUTATION DETECTOR
    Compares two claim versions and produces structured change signals,
    color-coded diff tokens, and natural language explanations.
    """
    if dna1 is None:
        dna1 = extract_rumour_dna(text1)
    if dna2 is None:
        dna2 = extract_rumour_dna(text2)

    added_info: List[str] = []
    removed_info: List[str] = []
    changed_dates: List[Dict[str, Any]] = []
    changed_numbers: List[Dict[str, Any]] = []
    changed_locations: List[Dict[str, Any]] = []
    changed_entities: List[Dict[str, Any]] = []
    missing_conditions: List[str] = []
    unsupported_additions: List[str] = []

    # 1. Dates comparison
    d1 = set([e.name.lower() for e in dna1.entities if e.category == "date"])
    d2 = set([e.name.lower() for e in dna2.entities if e.category == "date"])
    if d1 != d2 and (d1 or d2):
        changed_dates.append({
            "original": list(d1) if d1 else ["unspecified date"],
            "modified": list(d2) if d2 else ["date omitted"]
        })

    # 2. Numbers comparison
    n1 = set([e.name.lower() for e in dna1.entities if e.category == "quantity"])
    n2 = set([e.name.lower() for e in dna2.entities if e.category == "quantity"])
    if n1 != n2 and (n1 or n2):
        changed_numbers.append({
            "original": list(n1) if n1 else ["none stated"],
            "modified": list(n2) if n2 else ["omitted"]
        })

    # 3. Locations comparison
    l1 = set([e.name.lower() for e in dna1.entities if e.category == "location"])
    l2 = set([e.name.lower() for e in dna2.entities if e.category == "location"])
    if l1 != l2 and (l1 or l2):
        changed_locations.append({
            "original": list(l1) if l1 else ["unspecified"],
            "modified": list(l2) if l2 else ["unspecified"]
        })

    # 4. People/Orgs comparison
    o1 = set([e.name.lower() for e in dna1.entities if e.category in ("organization", "person")])
    o2 = set([e.name.lower() for e in dna2.entities if e.category in ("organization", "person")])
    if o1 != o2 and (o1 or o2):
        changed_entities.append({
            "original": list(o1) if o1 else ["none"],
            "modified": list(o2) if o2 else ["none"]
        })

    # 5. Scope change
    rank1 = SCOPE_RANK.get(dna1.scope, 2)
    rank2 = SCOPE_RANK.get(dna2.scope, 2)
    if rank2 > rank1:
        scope_direction = "expanded"
    elif rank2 < rank1:
        scope_direction = "narrowed"
    else:
        scope_direction = "unchanged"
    
    scope_change = {
        "from": dna1.scope,
        "to": dna2.scope,
        "direction": scope_direction
    }

    # 6. Condition keywords removed (Missing conditions)
    lower1 = text1.lower()
    lower2 = text2.lower()
    for cw in CONDITION_WORDS:
        if re.search(r'\b' + re.escape(cw) + r'\b', lower1) and not re.search(r'\b' + re.escape(cw) + r'\b', lower2):
            missing_conditions.append(cw)

    # 7. Unsupported additions / escalating modifiers
    for esc in MISLEADING_ESCALATIONS:
        if re.search(r'\b' + re.escape(esc) + r'\b', lower2) and not re.search(r'\b' + re.escape(esc) + r'\b', lower1):
            unsupported_additions.append(esc)

    # 8. Token-level Sequence Differencing with 4-Color Logic:
    # Green = added information
    # Red = removed information
    # Amber = potentially misleading change (scope escalation, alarming claims, stripped caveat)
    # Blue = contextual modification (rephrasing, connective words)
    words1 = text1.split()
    words2 = text2.split()
    matcher = difflib.SequenceMatcher(None, words1, words2)
    diff_tokens: List[MutationDiffToken] = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            diff_tokens.append(MutationDiffToken(
                type="equal",
                text=" ".join(words2[j1:j2])
            ))
        elif tag == 'insert':
            inserted_chunk = " ".join(words2[j1:j2])
            added_info.append(inserted_chunk)
            # Check if inserted chunk has misleading / escalation terms
            has_escalation = any(term in inserted_chunk.lower().split() for term in MISLEADING_ESCALATIONS)
            if has_escalation or (scope_direction == "expanded" and any(w in inserted_chunk.lower() for w in ["all", "entire", "state", "national"])):
                diff_tokens.append(MutationDiffToken(type="misleading", text=inserted_chunk))
            else:
                diff_tokens.append(MutationDiffToken(type="added", text=inserted_chunk))
        elif tag == 'delete':
            deleted_chunk = " ".join(words1[i1:i2])
            removed_info.append(deleted_chunk)
            # Check if deleted chunk removed a crucial condition
            has_condition = any(term in deleted_chunk.lower() for term in CONDITION_WORDS)
            if has_condition:
                diff_tokens.append(MutationDiffToken(type="misleading", text=f"[-{deleted_chunk}-]"))
            else:
                diff_tokens.append(MutationDiffToken(type="removed", text=f"[-{deleted_chunk}-]"))
        elif tag == 'replace':
            old_chunk = " ".join(words1[i1:i2])
            new_chunk = " ".join(words2[j1:j2])
            removed_info.append(old_chunk)
            added_info.append(new_chunk)
            
            # Check if replace changes meaning dramatically
            if any(term in new_chunk.lower() for term in MISLEADING_ESCALATIONS) or any(term in old_chunk.lower() for term in CONDITION_WORDS):
                diff_tokens.append(MutationDiffToken(type="misleading", text=new_chunk))
            else:
                diff_tokens.append(MutationDiffToken(type="context", text=new_chunk))

    # 9. Build Natural Language Explanation
    explanation_parts = []
    
    if scope_direction == "expanded":
        explanation_parts.append(
            f"The scope expanded from {dna1.scope} to {dna2.scope}."
        )
    elif scope_direction == "narrowed":
        explanation_parts.append(
            f"The scope was narrowed from {dna1.scope} to {dna2.scope}."
        )

    if changed_numbers:
        orig_nums = ", ".join(changed_numbers[0]["original"])
        mod_nums = ", ".join(changed_numbers[0]["modified"])
        explanation_parts.append(f"Numbers changed from '{orig_nums}' to '{mod_nums}'.")

    if changed_dates:
        orig_d = ", ".join(changed_dates[0]["original"])
        mod_d = ", ".join(changed_dates[0]["modified"])
        explanation_parts.append(f"Dates changed from '{orig_d}' to '{mod_d}'.")

    if missing_conditions:
        explanation_parts.append(
            f"Key qualifying conditions were removed ({', '.join(missing_conditions)}), making the revised statement appear broader than originally stated."
        )

    if unsupported_additions:
        explanation_parts.append(
            f"New escalating terms were introduced ({', '.join(unsupported_additions)})."
        )

    if not explanation_parts:
        if added_info or removed_info:
            explanation_parts.append("Minor stylistic or phrasing adjustments were made without altering the core factual context.")
        else:
            explanation_parts.append("Both versions are semantically and factually identical.")

    explanation_text = " ".join(explanation_parts)
    has_mutation = bool(added_info or removed_info or changed_dates or changed_numbers or scope_direction != "unchanged")

    return MutationReportSchema(
        has_mutation=has_mutation,
        added_information=added_info[:5],
        removed_information=removed_info[:5],
        changed_dates=changed_dates,
        changed_numbers=changed_numbers,
        changed_locations=changed_locations,
        changed_entities=changed_entities,
        scope_change=scope_change,
        missing_conditions=missing_conditions,
        unsupported_additions=unsupported_additions,
        diff_tokens=diff_tokens,
        explanation=explanation_text
    )
