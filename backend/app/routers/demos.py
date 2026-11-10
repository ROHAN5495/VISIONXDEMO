import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from backend.app.database import get_db
from backend.app.models.investigation import Investigation, ClaimVersion, EvidenceRecord
from backend.app.services.demo_data import DEMO_INVESTIGATIONS, build_demo_investigation

router = APIRouter(prefix="/api/demos", tags=["Demonstration Mode"])

@router.get("", response_model=List[Dict[str, Any]])
def list_demonstrations():
    """
    Returns the list of 3 prepared demonstration investigations.
    Clearly marks demonstration status.
    """
    summaries = []
    for d in DEMO_INVESTIGATIONS:
        summaries.append({
            "demo_id": d["demo_id"],
            "title": d["title"],
            "category": d["category"],
            "summary": d["summary"],
            "version_count": len(d["versions"]),
            "is_demo": True
        })
    return summaries

@router.get("/{demo_id}")
def get_demo_detail(demo_id: str, db: Session = Depends(get_db)):
    """
    Loads an interactive prepared demo investigation.
    If not already in DB, seeds it and returns it.
    """
    existing = db.query(Investigation).filter(Investigation.demo_id == demo_id).first()
    if existing:
        return existing

    raw_demo = next((d for d in DEMO_INVESTIGATIONS if d["demo_id"] == demo_id), None)
    if not raw_demo:
        raise HTTPException(status_code=404, detail=f"Demo '{demo_id}' not found.")

    built = build_demo_investigation(raw_demo)
    
    # Save to DB
    inv = Investigation(
        id=str(uuid.uuid4()),
        title=built["title"],
        summary=built["summary"],
        is_demo=True,
        demo_id=built["demo_id"],
        verdict=built["verdict"],
        score=built["score"],
        score_breakdown=built["score_breakdown"],
        human_explanation=built["human_explanation"],
        status="completed",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(inv)
    db.flush()

    # Add versions
    prev_vid = None
    for v_data in built["versions"]:
        cv = ClaimVersion(
            id=str(uuid.uuid4()),
            investigation_id=inv.id,
            version_number=v_data["version_number"],
            claim_text=v_data["claim_text"],
            source_origin=v_data["source_origin"],
            recorded_date=v_data["recorded_date"],
            origin_type=v_data["origin_type"],
            evidence_status=v_data["evidence_status"],
            dna=v_data["dna"],
            changes_from_previous=v_data["changes_from_previous"],
            parent_version_id=prev_vid
        )
        db.add(cv)
        db.flush()
        prev_vid = cv.id

    # Add evidence
    for e_data in built["evidence"]:
        ev = EvidenceRecord(
            id=str(uuid.uuid4()),
            investigation_id=inv.id,
            url=e_data["url"],
            publisher=e_data["publisher"],
            title=e_data["title"],
            publication_date=e_data["publication_date"],
            retrieval_date=e_data["retrieval_date"],
            excerpt=e_data["excerpt"],
            classification=e_data["classification"],
            relevance_reason=e_data["relevance_reason"],
            reliability_score=e_data["reliability_score"],
            is_demo=True,
            is_independent=e_data["is_independent"]
        )
        db.add(ev)

    db.commit()
    db.refresh(inv)
    return inv

@router.post("/seed")
def seed_all_demos(db: Session = Depends(get_db)):
    """Seeds all 3 demonstration investigations into the database."""
    seeded = []
    for raw_demo in DEMO_INVESTIGATIONS:
        existing = db.query(Investigation).filter(Investigation.demo_id == raw_demo["demo_id"]).first()
        if not existing:
            built = build_demo_investigation(raw_demo)
            inv = Investigation(
                id=str(uuid.uuid4()),
                title=built["title"],
                summary=built["summary"],
                is_demo=True,
                demo_id=built["demo_id"],
                verdict=built["verdict"],
                score=built["score"],
                score_breakdown=built["score_breakdown"],
                human_explanation=built["human_explanation"],
                status="completed"
            )
            db.add(inv)
            db.flush()
            
            prev_vid = None
            for v_data in built["versions"]:
                cv = ClaimVersion(
                    id=str(uuid.uuid4()),
                    investigation_id=inv.id,
                    version_number=v_data["version_number"],
                    claim_text=v_data["claim_text"],
                    source_origin=v_data["source_origin"],
                    recorded_date=v_data["recorded_date"],
                    origin_type=v_data["origin_type"],
                    evidence_status=v_data["evidence_status"],
                    dna=v_data["dna"],
                    changes_from_previous=v_data["changes_from_previous"],
                    parent_version_id=prev_vid
                )
                db.add(cv)
                db.flush()
                prev_vid = cv.id
                
            for e_data in built["evidence"]:
                ev = EvidenceRecord(
                    id=str(uuid.uuid4()),
                    investigation_id=inv.id,
                    url=e_data["url"],
                    publisher=e_data["publisher"],
                    title=e_data["title"],
                    publication_date=e_data["publication_date"],
                    retrieval_date=e_data["retrieval_date"],
                    excerpt=e_data["excerpt"],
                    classification=e_data["classification"],
                    relevance_reason=e_data["relevance_reason"],
                    reliability_score=e_data["reliability_score"],
                    is_demo=True,
                    is_independent=e_data["is_independent"]
                )
                db.add(ev)
            db.commit()
            seeded.append(raw_demo["demo_id"])
    return {"message": "Demos ready", "seeded": seeded}
