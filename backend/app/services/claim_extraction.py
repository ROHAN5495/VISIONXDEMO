import re
import hashlib
from typing import Dict, Any, List
from backend.app.schemas.claim import RumourDNASchema
from backend.app.services.entity_extraction import extract_entities

STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "as", "at", "be", "because", "been", "before", "being", "below",
    "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down",
    "during", "each", "few", "for", "from", "further", "had", "has", "have", "having",
    "he", "her", "here", "hers", "herself", "him", "himself", "his", "how", "i", "if",
    "in", "into", "is", "it", "its", "itself", "me", "more", "most", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "she", "should", "so",
    "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves",
    "then", "there", "these", "they", "this", "those", "through", "to", "too", "under",
    "until", "up", "very", "was", "we", "were", "what", "when", "where", "which",
    "while", "who", "whom", "why", "with", "would", "you", "your", "yours"
}

SCOPE_INDICATORS = {
    "global": ["worldwide", "world", "globally", "all nations", "every country", "humanity"],
    "national": ["country", "nationwide", "all citizens", "across the country", "federal", "national", "government of india", "us government"],
    "statewide": ["state", "statewide", "all schools in the state", "entire state", "across the state", "state government", "province"],
    "district": ["district", "county", "metro", "citywide", "all schools in the district", "across the city"],
    "local": ["local", "neighborhood", "area", "community", "campus", "zone"],
    "specific": ["a school", "one school", "single", "particular", "st.", "dr.", "mr.", "mrs.", "individual", "this institution", "one patient"]
}

def normalize_text(text: str) -> str:
    """Normalizes text by lowercasing, removing punctuation, and trimming extra spaces."""
    cleaned = re.sub(r'[^\w\s]', ' ', text.lower())
    words = [w for w in cleaned.split() if w]
    return " ".join(words)

def extract_scope(text: str) -> str:
    """Determines the geographical or demographic scope of the claim."""
    lower = text.lower()
    
    # Check universal quantifiers first: if they say all/every schools, it's statewide or district
    if re.search(r'\b(all|every|entire)\s+schools\s+in\s+the\s+state\b', lower):
        return "statewide"
    if re.search(r'\b(all|every|entire)\s+schools\s+in\s+the\s+district\b', lower):
        return "district"
    if "statewide" in lower or "entire state" in lower or "across the state" in lower:
        return "statewide"
    if "district" in lower or "county" in lower:
        return "district"

    for scope, keywords in SCOPE_INDICATORS.items():
        for kw in keywords:
            if kw in lower:
                return scope
    
    # Specific institution indicators (e.g. "Oakridge High School", "St. Jude", single campus)
    if re.search(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:High School|School|Hospital|Clinic|Campus|University|College)\b', text):
        return "specific"

    if re.search(r'\b(all|every|entire|universal)\b', lower):
        if "school" in lower or "college" in lower or "hospital" in lower:
            return "statewide"
        return "national"
    
    if re.search(r'\b(a|one|single|individual)\b', lower):
        return "specific"

    return "general"

def extract_subject(text: str, entities: List[Any]) -> str:
    """Identifies the primary subject or topic of the claim."""
    lower = text.lower()
    
    # Priority subjects in common public rumours & verifiable facts
    key_topics = [
        ("school closure", ["school", "schools", "holiday", "closed", "closure", "classes", "education"]),
        ("public health", ["vaccine", "virus", "infection", "hospital", "patient", "cure", "medicine", "fda", "who"]),
        ("astronomy & science", ["sun", "earth", "moon", "solar", "planet", "orbit", "rotation", "rises", "stars", "gravity"]),
        ("government policy", ["government", "order", "ministry", "subsidy", "grant", "tax", "ban", "scheme"]),
        ("weather & disaster", ["flood", "cyclone", "earthquake", "warning", "evacuation", "storm"]),
        ("elections & politics", ["election", "vote", "voter", "ballot", "candidate", "polling"]),
        ("finance & relief", ["bank", "currency", "relief fund", "payment", "pension", "bonus"])
    ]
    
    for topic, words in key_topics:
        match_count = sum(1 for w in words if w in lower)
        if match_count >= 2:
            return topic.title()
    
    # If specific org or person entity found, use that
    for ent in entities:
        if ent.category in ("organization", "person", "event"):
            return ent.name
            
    # Fallback to first non-stopword significant chunk
    words = [w for w in re.sub(r'[^\w\s]', '', text).split() if w.lower() not in STOPWORDS]
    if len(words) >= 2:
        return f"{words[0].capitalize()} {words[1].capitalize()}"
    elif len(words) == 1:
        return words[0].capitalize()
    return "Public Statement"

def extract_factual_assertion(text: str) -> str:
    """
    Synthesizes the core factual predicate of the claim.
    Converts question forms and conversational forwarding prefixes into declarative assertions.
    """
    text_clean = text.strip()
    # Remove leading conversational intros e.g. "Just received:", "Forwarded as received:", "Urgent:"
    text_clean = re.sub(
        r'^(?:forwarded as received|urgent notice|breaking news|just in|alert|fyi|rumor has it that)[:\s-]+',
        '',
        text_clean,
        flags=re.IGNORECASE
    ).strip()

    # Convert common question openers into declarative assertions
    text_clean = re.sub(
        r'^(?:is\s+it\s+true\s+that|is\s+it\s+a\s+fact\s+that|is\s+it\s+confirmed\s+that|can\s+you\s+verify\s+if)\s+',
        '',
        text_clean,
        flags=re.IGNORECASE
    )
    # Strip leading auxiliary question words: "Does the Sun rise in the east?" -> "The Sun rises in the east"
    text_clean = re.sub(r'^(?:does|did|do|is|are|will|can|should|would)\s+', '', text_clean, flags=re.IGNORECASE)
    
    # Strip trailing question marks and punctuation noise
    text_clean = text_clean.rstrip('?').strip()
    
    # Take the first main sentence
    sentences = re.split(r'[.!?]+', text_clean)
    first_sentence = sentences[0].strip() if sentences else text_clean
    return first_sentence if len(first_sentence) > 5 else text_clean

def compute_semantic_hash(normalized_text: str) -> str:
    """Computes a stable hash based on normalized informative keywords."""
    tokens = [w for w in normalized_text.split() if w not in STOPWORDS]
    tokens.sort()
    keyword_str = " ".join(tokens)
    return hashlib.sha256(keyword_str.encode('utf-8')).hexdigest()[:16]

def extract_rumour_dna(claim_text: str) -> RumourDNASchema:
    """
    FEATURE A — RUMOUR DNA
    Creates a unique fingerprint for a claim version.
    """
    normalized = normalize_text(claim_text)
    entities = extract_entities(claim_text)
    
    # Extract distinct numbers and stats
    numbers_stats = [e.name for e in entities if e.category == "quantity"]
    
    # Extract location if found
    locations = [e.name for e in entities if e.category == "location"]
    primary_location = locations[0] if locations else None
    
    # Extract date/time if found
    dates = [e.name for e in entities if e.category == "date"]
    primary_date = dates[0] if dates else None
    
    scope = extract_scope(claim_text)
    subject = extract_subject(claim_text, entities)
    assertion = extract_factual_assertion(claim_text)
    semantic_hash = compute_semantic_hash(normalized)
    is_negated = bool(re.search(r"\b(not|never|no|false|fake|untrue|neither|nor|cannot|isn't|aren't|doesn't|don't|won't)\b", normalized))
    
    return RumourDNASchema(
        subject=subject,
        entities=entities,
        location=primary_location,
        date_time=primary_date,
        numbers_stats=numbers_stats,
        scope=scope,
        is_negated=is_negated,
        factual_assertion=assertion,
        semantic_hash=semantic_hash,
        normalized_text=normalized
    )
