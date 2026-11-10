import re
from typing import List, Dict, Any, Tuple, Set
from backend.app.schemas.claim import EvidenceRecordSchema, RumourDNASchema

ATTRIBUTE_ANTONYMS: Dict[str, str] = {
    'east': 'west', 'west': 'east',
    'eastern': 'western', 'western': 'eastern',
    'north': 'south', 'south': 'north',
    'northern': 'southern', 'southern': 'northern',
    'open': 'closed', 'closed': 'open',
    'opening': 'closing', 'closing': 'opening',
    'safe': 'dangerous', 'dangerous': 'safe',
    'toxic': 'safe', 'hazardous': 'safe',
    'legal': 'illegal', 'illegal': 'legal',
    'approved': 'unapproved', 'unapproved': 'approved',
    'authorized': 'unauthorized', 'unauthorized': 'authorized',
    'true': 'false', 'false': 'true',
    'increase': 'decrease', 'decrease': 'increase',
    'mandatory': 'optional', 'optional': 'mandatory',
    'all': 'only', 'universal': 'restricted'
}

VERB_ANTONYMS: Dict[str, str] = {
    'rise': 'set', 'rises': 'sets', 'rising': 'setting', 'rose': 'set',
    'set': 'rise', 'sets': 'rises', 'setting': 'rising'
}

REFUTATION_PATTERNS = [
    r'\b(?:refute[sd]?|refuting|debunk(?:ed|s|ing)?|denie[sd]|deny(?:ing)?|disprove[sd]?|disproving)\b',
    r'\b(?:hoax|myth|untrue|fabricated|unfounded|baseless|fake|false|incorrect)\b',
    r'\bno\s+(?:evidence|truth|proof|record|basis)\b',
    r'\bwarning\s+against\b'
]

NEGATION_PATTERNS = [
    r'\b(?:not|n\'t|never|neither|nor|false|untrue|myth|hoax|incorrect|denied|refuted|no\s+(?!matter|doubt|wonder))\b',
    r'\bhas\s+not\s+(?:been|received|declared|ordered|occurred)\b',
    r'\bno\s+(?:such|statewide|universal|general|district-wide|evidence|record)\b',
    r'\bnot\s+an?\s+(?:unconditional|approved|real|actual)\b',
    r'\bcontrary\s+to\s+(?:claims|reports|posts)\b',
    r'\bno\s+truth\s+to\b',
    r'\bwarning\s+against\b'
]

SCOPE_RESTRICTION_PATTERNS = [
    r'\bonly\s+[a-z0-9\s]+\s+was\b',
    r'\brestricted\s+exclusively\b',
    r'\bno\s+statewide\b',
    r'\bno\s+district-wide\b',
    r'\bisolated\s+incident\b',
    r'\bexclusive\s+to\b'
]

STOPWORDS = {
    'the', 'and', 'for', 'with', 'that', 'this', 'from', 'our', 'are', 'was',
    'were', 'has', 'have', 'had', 'been', 'will', 'shall', 'would', 'could',
    'should', 'can', 'may', 'might', 'must', 'does', 'did', 'due', 'until',
    'about', 'into', 'over', 'after', 'beneath', 'under', 'above', 'their',
    'there', 'these', 'those', 'also', 'just', 'more', 'some', 'any', 'is', 'a', 'an'
}

def stem_word(w: str) -> str:
    """Basic structural stemmer for suffix-invariant semantic matching."""
    w = w.lower()
    for suffix in ('ing', 'ed', 'es', 's'):
        if w.endswith(suffix) and len(w) > len(suffix) + 2:
            return w[:-len(suffix)]
    return w

def extract_assertion_keywords(assertion: str) -> List[str]:
    """Extracts non-stopword content tokens from the factual assertion."""
    tokens = re.findall(r'\b[a-zA-Z]{3,}\b', assertion.lower())
    return [w for w in tokens if w not in STOPWORDS and w not in ('not', 'never', 'neither', 'nor', 'false')]

def is_text_negated(text: str) -> bool:
    """Checks if text contains semantic or syntactic negation markers."""
    return any(re.search(pat, text.lower()) for pat in NEGATION_PATTERNS)

def is_sentence_question(s: str) -> bool:
    """Detects whether a sentence or heading is formatted as a question or inquiry."""
    s_clean = re.sub(r'^[#*_\-\s]+', '', s).strip().lower()
    return s_clean.endswith('?') or s_clean.startswith((
        'can ', 'does ', 'is ', 'will ', 'did ', 'could ', 'why ', 'how ', 'what ', 'where ', 'who ', 'when ', 'should ', 'would '
    ))

def check_bound_phrase(verb: str, attr: str, text: str) -> bool:
    """Checks if verb and attribute are bound within a prepositional or directional phrase."""
    v_stem = stem_word(verb)
    # Forward: 'appears to rise in the east', 'rises in the east', 'sets in the west'
    pat1 = r'\b' + re.escape(v_stem) + r'\w*\s+(?:(?:appears?\s+to\s+)?(?:in|from|to|at|towards?|into|on|for|as)?\s+(?:the\s+|a\s+|an\s+)?)\b' + re.escape(attr) + r'\b'
    # Reverse: 'eastern horizon sunrise'
    pat2 = r'\b' + re.escape(attr) + r'\b\s+(?:horizon\s+|direction\s+)?\b' + re.escape(v_stem) + r'\w*\b'
    return bool(re.search(pat1, text) or re.search(pat2, text))

def classify_single_record(claim_dna: RumourDNASchema, rec: EvidenceRecordSchema) -> Tuple[str, str]:
    """
    Evaluates an evidence record against the claim DNA and factual assertion.
    Distinguishes:
    - SUPPORTING: Directly confirms the factual assertion and polarity.
    - CONTRADICTORY: Directly refutes the assertion, exhibits polarity clash, or states opposing directional/factual values.
    - CONTEXTUAL: Discusses the subject but does not confirm or refute the specific predicate.
    - IRRELEVANT: Does not address the subject, entities, or factual predicate of the claim.
    """
    assertion = claim_dna.factual_assertion or claim_dna.normalized_text
    claim_scope = (claim_dna.scope or 'general').lower()
    claim_is_negated = is_text_negated(assertion)

    claim_keywords = extract_assertion_keywords(assertion)
    claim_stems = [stem_word(k) for k in claim_keywords]

    title = rec.title or ""
    excerpt = rec.excerpt or ""
    combined_text = f"{title}. {excerpt}".lower()
    
    # 1. Relevance check: Does evidence mention subject, entities, or assertion keywords?
    subject = (claim_dna.subject or "").lower()
    subj_tokens = [w for w in re.findall(r'\b[a-zA-Z]{3,}\b', subject) if w not in STOPWORDS]
    entity_names = [e.name.lower() for e in (claim_dna.entities or [])]
    entity_tokens = [w for ent in entity_names for w in re.findall(r'\b[a-zA-Z]{3,}\b', ent) if w not in STOPWORDS]

    has_subject = any(st in combined_text for st in subj_tokens) if subj_tokens else False
    has_entity = any(et in combined_text for et in entity_tokens) if entity_tokens else False
    token_overlap_count = sum(1 for k in claim_keywords if k in combined_text or stem_word(k) in combined_text)

    if not has_subject and not has_entity and token_overlap_count == 0:
        return (
            "irrelevant",
            "Unrelated source: does not address the subject, entities, or factual claim."
        )

    # 2. Scope restriction refutation:
    # If the claim asserts broad universal scope ('all schools', 'statewide', 'national')
    # but evidence specifies that only a single isolated site was involved.
    is_broad_claim = (claim_scope in ('statewide', 'national', 'district') or 
                      any(w in assertion.lower() for w in ('all', 'every', 'statewide', 'nationwide', 'universal')))
    if is_broad_claim and any(re.search(pat, combined_text) for pat in SCOPE_RESTRICTION_PATTERNS):
        return (
            "contradictory",
            "Contradicts the broad scope of the claim by documenting that the event was strictly restricted to a single site or group."
        )

    # 3. Explicit Refutation / Fact-Check Terms check:
    # Identifies explicit fact checks, denials, and debunks targeting the claim
    has_refutation = any(re.search(pat, combined_text) for pat in REFUTATION_PATTERNS)
    if has_refutation and (token_overlap_count >= 2 or (has_subject and token_overlap_count >= 1)):
        if not claim_is_negated:
            return (
                "contradictory",
                f"Directly refutes the claim: authoritative record debunks or denies the stated assertion."
            )
        else:
            return (
                "supporting",
                f"Corroborates the negative claim by confirming that the assertion was officially refuted or debunked."
            )

    # 4. Antonym / Directional / State opposition check:
    # Checks if evidence binds the claim predicate to an opposing attribute (e.g. 'rises in the east' vs 'rises in the west')
    # Or binds an opposing verb to the attribute (e.g. 'sets in the west' vs 'rises in the west')
    for kw in claim_keywords:
        if kw in ATTRIBUTE_ANTONYMS:
            opp_attr = ATTRIBUTE_ANTONYMS[kw]
            
            # Check if any action verb in the claim is bound to opp_attr in the text
            # e.g., claim has 'rise' and 'west', text has 'rise in the east'
            for action in claim_keywords:
                action_stem = stem_word(action)
                if action_stem != stem_word(kw) and action_stem not in ('sun', 'school', 'patient', 'hospital', 'college'):
                    if check_bound_phrase(action, opp_attr, combined_text):
                        # Only contradictory if the text does NOT also affirmatively state the claim attribute!
                        if not check_bound_phrase(action, kw, combined_text):
                            if not claim_is_negated:
                                return (
                                    "contradictory",
                                    f"Directly contradicts the claim by asserting an opposing factual property ('{opp_attr}' instead of '{kw}')."
                                )
                            else:
                                return (
                                    "supporting",
                                    f"Supports the negative assertion by confirming that the opposing condition ('{opp_attr}') applies."
                                )

            # Check if an opposing verb is bound to kw in the text
            # e.g., claim has 'rise' and 'west', text has 'set in the west'
            for action in claim_keywords:
                if action in VERB_ANTONYMS:
                    opp_verb = VERB_ANTONYMS[action]
                    if check_bound_phrase(opp_verb, kw, combined_text):
                        if not check_bound_phrase(action, kw, combined_text):
                            if not claim_is_negated:
                                return (
                                    "contradictory",
                                    f"Directly contradicts the claim: documents '{opp_verb}' rather than '{action}' in connection with '{kw}'."
                                )
                            else:
                                return (
                                    "supporting",
                                    f"Supports the negative assertion by confirming '{opp_verb}' in connection with '{kw}'."
                                )

    # 5. Sentence-level Predicate and Polarity Matching:
    sentences = [s.strip() for s in re.split(r'[.!?\n]+', combined_text) if len(s.strip()) > 8]
    if not sentences:
        sentences = [combined_text]

    found_contradiction = False
    found_contradiction_reason = ""
    found_support = False
    found_support_reason = ""

    min_required = len(claim_keywords) - (0 if len(claim_keywords) <= 2 else 1)

    for sentence in sentences:
        s_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', sentence))
        s_stems = set(stem_word(w) for w in s_words)

        matched = [k for i, k in enumerate(claim_keywords) if k in s_words or claim_stems[i] in s_stems]
        overlap_count = len(matched)

        if overlap_count >= min_required and overlap_count >= 2:
            sentence_is_q = is_sentence_question(sentence)
            sentence_has_negation = is_text_negated(sentence)

            # Polarity alignment:
            if sentence_has_negation:
                if not claim_is_negated:
                    found_contradiction = True
                    found_contradiction_reason = f"Refutes the investigated statement: source explicitly negates or denies '{assertion[:50]}...'."
                else:
                    found_support = True
                    found_support_reason = f"Corroborates the negative statement by confirming the absence or refutation of '{assertion[:50]}...'."
            elif not sentence_is_q:
                # Declarative affirmative sentence
                if not claim_is_negated:
                    found_support = True
                    found_support_reason = f"Directly corroborates the factual assertion: text confirms '{assertion[:50]}...'."
                else:
                    found_contradiction = True
                    found_contradiction_reason = f"Contradicts the negative statement by affirming that '{assertion[:50]}...' is indeed factual."

    # Substantive contradiction takes precedence over neutral/question overlap
    if found_contradiction:
        return "contradictory", found_contradiction_reason
    if found_support:
        return "supporting", found_support_reason

    return "contextual", "Provides topical background on the subject but does not confirm or refute the specific assertion."

def assess_contradictions(claim_dna: RumourDNASchema, evidence_records: List[EvidenceRecordSchema]) -> List[EvidenceRecordSchema]:
    """
    Evaluates each evidence record against the claim DNA and factual assertion.
    Produces accurate classification ('supporting', 'contradictory', 'contextual', 'irrelevant')
    and natural, traceable relevance reasons.
    """
    updated_records = []
    
    for rec in evidence_records:
        classification, reason = classify_single_record(claim_dna, rec)
        rec.classification = classification
        rec.relevance_reason = reason
        updated_records.append(rec)
        
    return updated_records
