import re
from typing import List, Dict, Any
from backend.app.schemas.claim import NamedEntity

KNOWN_ORGS = [
    "WHO", "World Health Organization", "CDC", "FDA", "NASA", "ISRO",
    "UN", "United Nations", "Government", "Ministry", "Department",
    "Police", "High Court", "Supreme Court", "Parliament", "Senate",
    "Federal Reserve", "RBI", "Hospital", "School", "University",
    "Authority", "Commission", "Board of Education"
]

KNOWN_LOCATIONS = [
    "New York", "California", "Florida", "Texas", "London", "UK", "United States",
    "India", "Delhi", "Mumbai", "Karnataka", "Bengaluru", "Bangalore",
    "Florida", "Ohio", "Ontario", "Toronto", "Sydney", "Australia",
    "Tokyo", "Japan", "Paris", "France", "Berlin", "Germany", "District",
    "State", "County", "City", "Metro"
]

def extract_entities(text: str) -> List[NamedEntity]:
    """
    Extracts named entities (people, orgs, locations, dates, numbers)
    using pattern recognition and structural heuristics.
    """
    entities: List[NamedEntity] = []
    seen = set()

    def add_entity(name: str, category: str):
        cleaned = name.strip(" ,.;:\"'()[]{}")
        if cleaned and len(cleaned) > 1 and (cleaned.lower(), category) not in seen:
            seen.add((cleaned.lower(), category))
            entities.append(NamedEntity(name=cleaned, category=category))

    # 1. Dates and Time periods
    date_patterns = [
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s+\d{4})?\b',
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
        r'\b\d{4}\b',  # years like 2024, 2025, 2026
        r'\b(?:today|yesterday|tomorrow|next week|last month|this Monday|this Friday)\b',
        r'\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+(?:days?|weeks?|months?|years?|hours?)\b'
    ]
    for pattern in date_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            add_entity(match.group(0), "date")

    # 2. Numbers, Statistics, Percentages, Currencies
    num_patterns = [
        r'\b\$\s*[\d,]+(?:\.\d+)?(?:\s*(?:billion|million|trillion|k))?\b',
        r'\b(?:Rs\.?|INR|USD|EUR|GBP)\s*[\d,]+(?:\.\d+)?\b',
        r'\b\d+(?:\.\d+)?%\b',
        r'\b\d+(?:,\d+)*(?:\.\d+)?\s*(?:cases|deaths|people|students|schools|dollars|rupees|patients|doses|votes)\b',
        r'\b\d+(?:\.\d+)?\b'
    ]
    for pattern in num_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            val = match.group(0)
            # Skip if already captured as a 4-digit year
            if not (len(val) == 4 and val.isdigit() and 1900 <= int(val) <= 2100):
                add_entity(val, "quantity")

    # 3. Known Organizations
    for org in KNOWN_ORGS:
        if re.search(r'\b' + re.escape(org) + r'\b', text, re.IGNORECASE):
            add_entity(org, "organization")

    # 4. Known Locations
    for loc in KNOWN_LOCATIONS:
        if re.search(r'\b' + re.escape(loc) + r'\b', text, re.IGNORECASE):
            add_entity(loc, "location")

    # 5. Capitalized Proper Nouns / Names heuristic
    # Match sequences of capitalized words not at the beginning of sentence if possible
    words = text.split()
    for i, w in enumerate(words):
        w_clean = re.sub(r'^[^\w]+|[^\w]+$', '', w)
        if len(w_clean) > 2 and w_clean[0].isupper() and not w_clean.isupper():
            # Check if likely person/org not already in list
            if w_clean.lower() not in {"the", "a", "an", "this", "that", "these", "those", "all", "every", "some"}:
                # check if next word is also capitalized
                if i + 1 < len(words) and re.sub(r'^[^\w]+|[^\w]+$', '', words[i+1]).istitle():
                    compound = f"{w_clean} {re.sub(r'^[^\w]+|[^\w]+$', '', words[i+1])}"
                    add_entity(compound, "person")
                elif (w_clean.lower(), "person") not in seen and (w_clean.lower(), "location") not in seen and (w_clean.lower(), "organization") not in seen:
                    add_entity(w_clean, "entity")

    return entities
