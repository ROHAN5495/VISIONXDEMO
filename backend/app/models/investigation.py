import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, Text, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Investigation(Base):
    __tablename__ = "investigations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    is_demo = Column(Boolean, default=False, nullable=False)
    demo_id = Column(String(50), nullable=True)
    evidence_mode = Column(String(50), default="offline_demo", nullable=True)  # "live", "offline_demo", "mixed"
    
    verdict = Column(String(50), default="UNVERIFIED", nullable=False)
    confidence = Column(String(20), default="LOW", nullable=True)  # "HIGH", "MEDIUM", "LOW"
    analysis_mode = Column(String(50), default="offline_fallback", nullable=True)  # "live_search_ai", "live_search_rules", "offline_fallback"
    score = Column(Integer, nullable=True)  # None if insufficient evidence
    score_breakdown = Column(JSON, nullable=True)
    human_explanation = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    status = Column(String(50), default="completed", nullable=False)
    
    # Relationships
    versions = relationship("ClaimVersion", back_populates="investigation", cascade="all, delete-orphan", order_by="ClaimVersion.version_number")
    evidence = relationship("EvidenceRecord", back_populates="investigation", cascade="all, delete-orphan")

    @property
    def confidence_score(self):
        if self.score_breakdown and isinstance(self.score_breakdown, dict):
            return self.score_breakdown.get("confidence_score")
        return None

    @property
    def verdict_reason(self):
        if self.score_breakdown and isinstance(self.score_breakdown, dict):
            return self.score_breakdown.get("verdict_reason")
        return None

    @property
    def key_excerpts(self):
        if self.score_breakdown and isinstance(self.score_breakdown, dict):
            return self.score_breakdown.get("key_excerpts", [])
        return []

class ClaimVersion(Base):
    __tablename__ = "claim_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    investigation_id = Column(String(36), ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False)
    version_number = Column(Integer, default=1, nullable=False)
    claim_text = Column(Text, nullable=False)
    source_origin = Column(String(255), default="Direct Submission", nullable=False)
    recorded_date = Column(String(50), nullable=False)
    origin_type = Column(String(50), default="user_submitted", nullable=False)  # "observed", "user_submitted", "ai_inferred"
    evidence_status = Column(String(50), default="unverified", nullable=False)  # "supported", "contradicted", "unverified", "altered"
    
    # Feature A: Rumour DNA (JSON format containing extracted fingerprints)
    dna = Column(JSON, nullable=True)
    
    # Feature B: Mutation details relative to prior version
    changes_from_previous = Column(JSON, nullable=True)
    parent_version_id = Column(String(36), ForeignKey("claim_versions.id"), nullable=True)

    # Relationships
    investigation = relationship("Investigation", back_populates="versions")

class EvidenceRecord(Base):
    __tablename__ = "evidence_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    investigation_id = Column(String(36), ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False)
    claim_version_id = Column(String(36), nullable=True)
    
    url = Column(String(1000), nullable=False)
    publisher = Column(String(255), nullable=False)
    title = Column(String(500), nullable=False)
    publication_date = Column(String(50), nullable=True)
    retrieval_date = Column(String(50), nullable=False)
    excerpt = Column(Text, nullable=False)
    classification = Column(String(50), nullable=False)  # "supporting", "contradictory", "contextual"
    relevance_reason = Column(Text, nullable=False)
    reliability_score = Column(Integer, default=70, nullable=False)  # 0 to 100
    is_demo = Column(Boolean, default=False, nullable=False)
    is_independent = Column(Boolean, default=True, nullable=False)

    # Relationships
    investigation = relationship("Investigation", back_populates="evidence")
