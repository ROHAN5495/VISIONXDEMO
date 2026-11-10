from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from backend.app.schemas.claim import (
    RumourDNASchema,
    MutationReportSchema,
    CompareClaimsRequest
)
from backend.app.services.claim_extraction import extract_rumour_dna
from backend.app.services.mutation_analysis import analyze_mutations
from backend.app.services.semantic_comparison import are_claims_in_family, calculate_semantic_similarity
from backend.app.database import get_db
from backend.app.models.investigation import ClaimVersion

router = APIRouter(prefix="/api/claims", tags=["Claims & Analysis"])

@router.post("/dna", response_model=RumourDNASchema)
def get_claim_dna(payload: Dict[str, str]):
    """
    FEATURE A — RUMOUR DNA
    Generates a unique fingerprint for a given claim text.
    """
    text = payload.get("text", "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text field is required.")
    return extract_rumour_dna(text)

@router.post("/compare", response_model=MutationReportSchema)
def compare_claim_versions(req: CompareClaimsRequest):
    """
    FEATURE B — MUTATION DETECTOR
    Compares two claim versions side-by-side with 4-color coded tokens
    and ordinary language explanation.
    """
    dna1 = extract_rumour_dna(req.original_text)
    dna2 = extract_rumour_dna(req.modified_text)
    report = analyze_mutations(req.original_text, req.modified_text, dna1, dna2)
    return report

@router.get("/family/{version_id}")
def get_claim_family(version_id: str, db: Session = Depends(get_db)):
    """
    FEATURE A — RUMOUR DNA VISUAL FAMILY
    Discovers related claims in the database using semantic similarity and DNA overlap.
    """
    target = db.query(ClaimVersion).filter(ClaimVersion.id == version_id).first()
    if not target or not target.dna:
        raise HTTPException(status_code=404, detail="Claim version not found.")

    target_dna = RumourDNASchema(**target.dna)
    all_versions = db.query(ClaimVersion).filter(ClaimVersion.id != version_id).all()

    family_members = []
    for other in all_versions:
        if not other.dna:
            continue
        other_dna = RumourDNASchema(**other.dna)
        is_family, reason = are_claims_in_family(target_dna, other_dna)
        similarity = calculate_semantic_similarity(target.claim_text, other.claim_text, target_dna, other_dna)

        if is_family or similarity >= 0.35:
            family_members.append({
                "version_id": other.id,
                "investigation_id": other.investigation_id,
                "claim_text": other.claim_text,
                "subject": other_dna.subject,
                "scope": other_dna.scope,
                "similarity_score": similarity,
                "connection_reason": reason,
                "recorded_date": other.recorded_date
            })

    # Sort descending by similarity
    family_members.sort(key=lambda x: x["similarity_score"], reverse=True)
    return {
        "target_version_id": target.id,
        "target_subject": target_dna.subject,
        "family_members": family_members
    }
