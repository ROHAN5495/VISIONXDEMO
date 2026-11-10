import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.app.database import get_db
from backend.app.models.investigation import Investigation, ClaimVersion, EvidenceRecord
from backend.app.schemas.claim import (
    InvestigationCreateRequest,
    AddVersionRequest,
    InvestigationResponse,
    EvidenceRecordSchema
)
from backend.app.services.claim_extraction import extract_rumour_dna
from backend.app.services.mutation_analysis import analyze_mutations
from backend.app.services.evidence_search import search_live_evidence
from backend.app.services.contradiction_detection import assess_contradictions
from backend.app.services.credibility_scoring import calculate_evidence_score
from backend.app.services.report_generator import generate_human_explanation
from backend.app.services.ai_service import ai_service

router = APIRouter(prefix="/api/investigations", tags=["Investigations"])

@router.post("", response_model=InvestigationResponse)
def create_investigation(payload: InvestigationCreateRequest, db: Session = Depends(get_db)):
    """
    Executes the 10-step investigation workflow:
    SUBMIT -> UNDERSTAND -> RETRIEVE -> VERIFY -> COMPARE -> EXPLAIN -> TRACK
    """
    raw_text = payload.claim_text.strip()
    if not raw_text:
        raise HTTPException(status_code=400, detail="Claim text cannot be empty.")
    
    # Step 2: Understand & Extract DNA
    primary_dna = extract_rumour_dna(raw_text)
    
    # Step 3 & 4: Retrieve Evidence with optimized query
    query_str = primary_dna.factual_assertion
    if primary_dna.subject.lower() not in primary_dna.factual_assertion.lower():
        query_str = f"{primary_dna.subject} {primary_dna.factual_assertion}"

    evidence_results, is_live, search_status = search_live_evidence(query_str)
    
    # Step 5: Identify supporting, contradictory, contextual evidence
    assessed_evidence = assess_contradictions(primary_dna, evidence_results)
    
    # Determine accurate evidence mode and demo status
    has_live_ev = any(not e.is_demo for e in assessed_evidence)
    has_demo_ev = any(e.is_demo for e in assessed_evidence)

    if payload.is_demo:
        evidence_mode = "offline_demo"
        inv_is_demo = True
    elif has_live_ev and not has_demo_ev:
        evidence_mode = "live"
        inv_is_demo = False
    elif has_live_ev and has_demo_ev:
        evidence_mode = "mixed"
        inv_is_demo = False
    else:
        evidence_mode = "offline_demo"
        inv_is_demo = True

    # Check for Optional AI-Assisted Interpretation (Google Gemini)
    analysis_mode = "offline_fallback" if inv_is_demo else "live_search_rules"
    ai_truth_summary = None

    if is_live and not inv_is_demo and ai_service.is_available():
        ai_data, ai_success, ai_msg = ai_service.analyze_evidence(primary_dna, assessed_evidence)
        if ai_success and ai_data:
            analysis_mode = "live_search_ai"
            # Apply validated AI interpretations
            evaluations = ai_data.get("evaluations", [])
            for ev_eval in evaluations:
                idx = ev_eval.get("index")
                if isinstance(idx, int) and 0 <= idx < len(assessed_evidence):
                    rec = assessed_evidence[idx]
                    rec.classification = ev_eval.get("classification", rec.classification)
                    rec.relevance_reason = ev_eval.get("reason", rec.relevance_reason)
                    if ev_eval.get("supporting_quote"):
                        rec.supporting_quote = ev_eval.get("supporting_quote")
            if ai_data.get("truth_explanation"):
                ai_truth_summary = ai_data.get("truth_explanation")
    
    # Handle subsequent versions if supplied upfront
    versions_to_create = []
    
    # Version 1 (Root claim)
    v1_recorded_date = payload.recorded_date or datetime.utcnow().strftime("%Y-%m-%d")
    v1_origin_type = payload.origin_type or "user_submitted"
    v1_source = payload.source_origin or "Direct Submission"
    
    # Determine evidence status for V1
    supporting_count = sum(1 for e in assessed_evidence if e.classification == "supporting")
    contradictory_count = sum(1 for e in assessed_evidence if e.classification == "contradictory")
    
    if contradictory_count > supporting_count:
        v1_status = "contradicted"
    elif supporting_count > 0:
        v1_status = "supported"
    else:
        v1_status = "unverified"
        
    versions_to_create.append({
        "version_number": 1,
        "claim_text": raw_text,
        "source_origin": v1_source,
        "recorded_date": v1_recorded_date,
        "origin_type": v1_origin_type,
        "evidence_status": v1_status,
        "dna": primary_dna.model_dump(),
        "changes_from_previous": None
    })
    
    # Process any additional subsequent versions provided
    last_text = raw_text
    last_dna = primary_dna
    latest_mutation = None
    
    if payload.subsequent_versions:
        for idx, sub_v in enumerate(payload.subsequent_versions, start=2):
            sub_text = sub_v.get("claim_text", "").strip()
            if not sub_text:
                continue
            sub_dna = extract_rumour_dna(sub_text)
            mutation = analyze_mutations(last_text, sub_text, last_dna, sub_dna)
            latest_mutation = mutation
            
            sub_ev_status = "altered"
            if mutation.scope_change.get("direction") == "expanded":
                sub_ev_status = "contradicted"
                
            versions_to_create.append({
                "version_number": idx,
                "claim_text": sub_text,
                "source_origin": sub_v.get("source_origin", f"Forwarded Version {idx}"),
                "recorded_date": sub_v.get("recorded_date", datetime.utcnow().strftime("%Y-%m-%d")),
                "origin_type": sub_v.get("origin_type", "user_submitted"),
                "evidence_status": sub_ev_status,
                "dna": sub_dna.model_dump(),
                "changes_from_previous": mutation.model_dump()
            })
            last_text = sub_text
            last_dna = sub_dna

    # Target DNA is the latest version's DNA for final scoring & verdict
    target_dna = last_dna
    
    # Step 6 & 7: Score & Explanation
    score_breakdown = calculate_evidence_score(target_dna, assessed_evidence, analysis_mode=analysis_mode)
    
    if ai_truth_summary:
        human_explanation = ai_truth_summary
    else:
        human_explanation = generate_human_explanation(
            target_dna,
            assessed_evidence,
            score_breakdown,
            latest_mutation
        )
    
    # Step 8: Save to database
    inv_title = f"{primary_dna.subject}: {raw_text[:60]}..." if len(raw_text) > 60 else f"{primary_dna.subject}: {raw_text}"
    summary = f"Investigation into {primary_dna.subject} with {len(versions_to_create)} recorded version(s)."

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    inv = Investigation(
        id=str(uuid.uuid4()),
        title=inv_title,
        created_at=now,
        updated_at=now,
        is_demo=inv_is_demo,
        demo_id=None,
        evidence_mode=evidence_mode,
        verdict=score_breakdown.verdict,
        confidence=score_breakdown.confidence,
        analysis_mode=analysis_mode,
        score=score_breakdown.total_score,
        score_breakdown=score_breakdown.model_dump(),
        human_explanation=human_explanation,
        summary=summary,
        status="completed"
    )
    db.add(inv)
    db.flush()

    # Save Claim Versions with parent links
    prev_vid = None
    for v_info in versions_to_create:
        cv = ClaimVersion(
            id=str(uuid.uuid4()),
            investigation_id=inv.id,
            version_number=v_info["version_number"],
            claim_text=v_info["claim_text"],
            source_origin=v_info["source_origin"],
            recorded_date=v_info["recorded_date"],
            origin_type=v_info["origin_type"],
            evidence_status=v_info["evidence_status"],
            dna=v_info["dna"],
            changes_from_previous=v_info["changes_from_previous"],
            parent_version_id=prev_vid
        )
        db.add(cv)
        db.flush()
        prev_vid = cv.id

    # Save Evidence Records
    for ev_info in assessed_evidence:
        ev = EvidenceRecord(
            id=str(uuid.uuid4()),
            investigation_id=inv.id,
            url=ev_info.url,
            publisher=ev_info.publisher,
            title=ev_info.title,
            publication_date=ev_info.publication_date,
            retrieval_date=ev_info.retrieval_date,
            excerpt=ev_info.excerpt,
            classification=ev_info.classification,
            relevance_reason=ev_info.relevance_reason,
            reliability_score=ev_info.reliability_score,
            is_demo=ev_info.is_demo,
            is_independent=ev_info.is_independent
        )
        db.add(ev)

    db.commit()
    db.refresh(inv)
    return inv

@router.get("", response_model=List[InvestigationResponse])
def list_investigations(
    query: Optional[str] = None,
    verdict: Optional[str] = None,
    is_demo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Lists saved investigations with optional keyword or verdict filters."""
    q = db.query(Investigation)
    if is_demo is not None and isinstance(is_demo, bool):
        q = q.filter(Investigation.is_demo == is_demo)
    if verdict and isinstance(verdict, str):
        q = q.filter(Investigation.verdict == verdict)
    if query and isinstance(query, str):
        q = q.filter(Investigation.title.ilike(f"%{query}%"))
        
    investigations = q.order_by(Investigation.created_at.desc()).all()
    return investigations

@router.get("/{investigation_id}", response_model=InvestigationResponse)
def get_investigation(investigation_id: str, db: Session = Depends(get_db)):
    """Retrieves full investigation report including versions and evidence."""
    inv = db.query(Investigation).filter(Investigation.id == investigation_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Investigation not found.")
    return inv

@router.delete("/{investigation_id}")
def delete_investigation(investigation_id: str, db: Session = Depends(get_db)):
    """Deletes an investigation and all attached versions and evidence records."""
    inv = db.query(Investigation).filter(Investigation.id == investigation_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Investigation not found.")
    db.delete(inv)
    db.commit()
    return {"message": "Investigation deleted successfully.", "id": investigation_id}

@router.post("/{investigation_id}/versions", response_model=InvestigationResponse)
def add_claim_version(
    investigation_id: str,
    payload: AddVersionRequest,
    db: Session = Depends(get_db)
):
    """
    Adds a new evolutionary version to an existing claim timeline,
    automatically detects mutations against previous version, and updates verdict.
    """
    inv = db.query(Investigation).filter(Investigation.id == investigation_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Investigation not found.")

    new_text = payload.claim_text.strip()
    if not new_text:
        raise HTTPException(status_code=400, detail="Claim text is required.")

    # Get last version
    last_version = db.query(ClaimVersion).filter(
        ClaimVersion.investigation_id == investigation_id
    ).order_by(ClaimVersion.version_number.desc()).first()

    next_num = (last_version.version_number + 1) if last_version else 1
    new_dna = extract_rumour_dna(new_text)

    # Mutation against previous version
    mutation_data = None
    if last_version:
        last_dna = extract_rumour_dna(last_version.claim_text)
        mutation = analyze_mutations(last_version.claim_text, new_text, last_dna, new_dna)
        mutation_data = mutation.model_dump()

    # Determine status
    ev_status = "altered" if mutation_data and mutation_data.get("has_mutation") else "user_submitted"

    cv = ClaimVersion(
        id=str(uuid.uuid4()),
        investigation_id=inv.id,
        version_number=next_num,
        claim_text=new_text,
        source_origin=payload.source_origin or f"Forwarded Version {next_num}",
        recorded_date=payload.recorded_date or datetime.utcnow().strftime("%Y-%m-%d"),
        origin_type=payload.origin_type or "user_submitted",
        evidence_status=ev_status,
        dna=new_dna.model_dump(),
        changes_from_previous=mutation_data,
        parent_version_id=last_version.id if last_version else None
    )
    db.add(cv)

    # Re-evaluate evidence against the latest version's new DNA
    ev_records = [
        EvidenceRecordSchema(
            id=e.id,
            url=e.url,
            publisher=e.publisher,
            title=e.title,
            publication_date=e.publication_date,
            retrieval_date=e.retrieval_date,
            excerpt=e.excerpt,
            classification=e.classification,
            relevance_reason=e.relevance_reason,
            reliability_score=e.reliability_score,
            is_demo=e.is_demo,
            is_independent=e.is_independent
        )
        for e in inv.evidence
    ]

    assessed_ev_records = assess_contradictions(new_dna, ev_records)
    new_score = calculate_evidence_score(new_dna, assessed_ev_records, analysis_mode=inv.analysis_mode or "offline_fallback")
    latest_mut_obj = None
    if mutation_data:
        from backend.app.schemas.claim import MutationReportSchema
        latest_mut_obj = MutationReportSchema(**mutation_data)
        
    new_explanation = generate_human_explanation(new_dna, assessed_ev_records, new_score, latest_mut_obj)

    inv.verdict = new_score.verdict
    inv.confidence = new_score.confidence
    inv.score = new_score.total_score
    inv.score_breakdown = new_score.model_dump()
    inv.human_explanation = new_explanation
    inv.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)

    db.commit()
    db.refresh(inv)
    return inv
