from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

class NamedEntity(BaseModel):
    name: str
    category: str  # "person", "organization", "location", "date", "quantity", "event"

class RumourDNASchema(BaseModel):
    subject: str
    entities: List[NamedEntity] = []
    location: Optional[str] = None
    date_time: Optional[str] = None
    numbers_stats: List[str] = []
    scope: str = "specific"  # "specific", "local", "district", "regional", "statewide", "national", "global"
    is_negated: bool = False
    factual_assertion: str
    semantic_hash: str
    normalized_text: str

class MutationDiffToken(BaseModel):
    type: str  # "equal", "added" (green), "removed" (red), "misleading" (amber), "context" (blue)
    text: str

class MutationReportSchema(BaseModel):
    has_mutation: bool = False
    added_information: List[str] = []
    removed_information: List[str] = []
    changed_dates: List[Dict[str, Any]] = []
    changed_numbers: List[Dict[str, Any]] = []
    changed_locations: List[Dict[str, Any]] = []
    changed_entities: List[Dict[str, Any]] = []
    scope_change: Dict[str, Any] = {"from": "unknown", "to": "unknown", "direction": "unchanged"}
    missing_conditions: List[str] = []
    unsupported_additions: List[str] = []
    diff_tokens: List[MutationDiffToken] = []
    explanation: str = ""

class EvidenceRecordSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[str] = None
    investigation_id: Optional[str] = None
    claim_version_id: Optional[str] = None
    url: str
    publisher: str
    title: str
    publication_date: Optional[str] = None
    retrieval_date: str
    excerpt: str
    classification: str  # "supporting", "contradictory", "contextual", "irrelevant"
    relevance_reason: str
    reliability_score: int = 70
    is_demo: bool = False
    is_independent: bool = True
    is_snippet: bool = True
    supporting_quote: Optional[str] = None

class ClaimVersionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[str] = None
    investigation_id: Optional[str] = None
    version_number: int = 1
    claim_text: str
    source_origin: str = "Direct Submission"
    recorded_date: str
    origin_type: str = "user_submitted"  # "observed", "user_submitted", "ai_inferred"
    evidence_status: str = "unverified"
    dna: Optional[RumourDNASchema] = None
    changes_from_previous: Optional[MutationReportSchema] = None
    parent_version_id: Optional[str] = None

class ScoreBreakdownSchema(BaseModel):
    source_reliability: int
    direct_relevance: int
    independent_corroboration: int
    contradictory_penalty: int
    recency: int
    completeness: int
    total_score: Optional[int] = None
    verdict: str  # "LIKELY TRUE", "LIKELY FALSE", "MIXED / PARTIALLY TRUE", "UNVERIFIED"
    confidence: str = "LOW"  # "HIGH", "MEDIUM", "LOW"
    confidence_score: Optional[int] = None  # 0 to 100
    verdict_reason: str = ""
    analysis_mode: str = "offline_fallback"  # "live_search_ai", "live_search_rules", "offline_fallback"
    status_label: str
    explanation: str
    key_excerpts: List[Dict[str, Any]] = []

class InvestigationCreateRequest(BaseModel):
    claim_text: str = Field(..., min_length=5, description="The statement or rumour to investigate")
    source_origin: Optional[str] = Field("User submission", description="Source of claim, e.g., WhatsApp, X, Blog")
    origin_type: Optional[str] = Field("user_submitted", description="observed, user_submitted, or ai_inferred")
    recorded_date: Optional[str] = None
    is_demo: Optional[bool] = False
    subsequent_versions: Optional[List[Dict[str, Any]]] = None

class AddVersionRequest(BaseModel):
    claim_text: str = Field(..., min_length=5)
    source_origin: Optional[str] = "Follow-up forward"
    origin_type: Optional[str] = "user_submitted"
    recorded_date: Optional[str] = None

class CompareClaimsRequest(BaseModel):
    original_text: str = Field(..., min_length=3)
    modified_text: str = Field(..., min_length=3)

class InvestigationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    is_demo: bool
    demo_id: Optional[str] = None
    evidence_mode: Optional[str] = "offline_demo"  # "live", "offline_demo", "mixed"
    verdict: str
    confidence: Optional[str] = "LOW"
    confidence_score: Optional[int] = None
    verdict_reason: Optional[str] = None
    analysis_mode: Optional[str] = "offline_fallback"
    score: Optional[int] = None
    score_breakdown: Optional[Dict[str, Any]] = None
    human_explanation: Optional[str] = None
    summary: Optional[str] = None
    status: str
    key_excerpts: Optional[List[Dict[str, Any]]] = []
    versions: List[ClaimVersionSchema] = []
    evidence: List[EvidenceRecordSchema] = []
