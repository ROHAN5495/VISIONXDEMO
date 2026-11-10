import re
from typing import Dict, Any, List, Set, Tuple
from backend.app.schemas.claim import RumourDNASchema

def get_word_tokens(text: str) -> Set[str]:
    words = re.findall(r'\b[a-z0-9]+\b', text.lower())
    stopwords = {
        "a", "an", "the", "and", "or", "in", "on", "at", "to", "for", "with", "by", "of", "is", "are", "was", "were"
    }
    return {w for w in words if w not in stopwords}

def calculate_jaccard_similarity(set_a: Set[str], set_b: Set[str]) -> float:
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a.intersection(set_b))
    union = len(set_a.union(set_b))
    return float(intersection) / float(union) if union > 0 else 0.0

def calculate_semantic_similarity(text1: str, text2: str, dna1: RumourDNASchema = None, dna2: RumourDNASchema = None) -> float:
    """
    Computes a composite similarity score between 0.0 and 1.0 based on:
    - Keyword overlap (Jaccard)
    - Subject match
    - Named entity intersection
    - Scope alignment
    """
    tokens1 = get_word_tokens(text1)
    tokens2 = get_word_tokens(text2)
    jaccard = calculate_jaccard_similarity(tokens1, tokens2)

    score = jaccard * 0.6  # Base keyword weight

    if dna1 and dna2:
        # Subject match bonus
        if dna1.subject.lower() == dna2.subject.lower():
            score += 0.2
        elif any(w in dna2.subject.lower() for w in dna1.subject.lower().split()):
            score += 0.1

        # Entity overlap bonus
        e1 = {e.name.lower() for e in dna1.entities}
        e2 = {e.name.lower() for e in dna2.entities}
        if e1 and e2:
            ent_jaccard = calculate_jaccard_similarity(e1, e2)
            score += ent_jaccard * 0.2
    
    return min(1.0, round(score, 3))

def are_claims_in_family(dna1: RumourDNASchema, dna2: RumourDNASchema) -> Tuple[bool, str]:
    """
    Determines if two claims belong in the same visual rumour family.
    Rule: Do not assume similar wording means identical facts.
    """
    # 1. Exact or near subject match
    subject_match = (dna1.subject.lower() == dna2.subject.lower())
    
    # 2. Shared entities (location or org or person)
    e1_names = {e.name.lower() for e in dna1.entities}
    e2_names = {e.name.lower() for e in dna2.entities}
    shared_entities = e1_names.intersection(e2_names)
    
    # 3. Keyword similarity
    tokens1 = get_word_tokens(dna1.normalized_text)
    tokens2 = get_word_tokens(dna2.normalized_text)
    keyword_sim = calculate_jaccard_similarity(tokens1, tokens2)

    if subject_match and (shared_entities or keyword_sim > 0.25):
        reason = f"Shares core subject '{dna1.subject}' and overlapping factual context."
        return True, reason
        
    if shared_entities and keyword_sim > 0.3:
        reason = f"Shares verified entities ({', '.join(list(shared_entities)[:2])}) with related assertions."
        return True, reason
        
    if keyword_sim > 0.45:
        reason = "Substantial textual and semantic alignment detected."
        return True, reason

    return False, "Distinct subject and entity profiles."
