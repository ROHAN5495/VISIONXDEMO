import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from backend.app.database import init_db, SessionLocal
from backend.app.routers.investigations import (
    create_investigation,
    list_investigations,
    get_investigation,
    delete_investigation,
    add_claim_version
)
from backend.app.routers.claims import get_claim_dna, compare_claim_versions
from backend.app.routers.demos import list_demonstrations, get_demo_detail, seed_all_demos
from backend.app.schemas.claim import (
    InvestigationCreateRequest,
    AddVersionRequest,
    CompareClaimsRequest
)
from backend.app.main import health_check

@pytest.fixture(scope="module")
def db_session():
    init_db()
    db = SessionLocal()
    yield db
    db.close()

def test_health_check_endpoint():
    res = health_check()
    assert res["status"] == "healthy"
    assert res["tagline"] == "VERIFY BEFORE YOU SHARE."

def test_empty_claim_validation():
    # Empty string should fail Pydantic validation (min_length=5)
    with pytest.raises(ValidationError):
        InvestigationCreateRequest(claim_text="")

def test_create_and_evolve_investigation(db_session):
    # 1. Create initial investigation
    req = InvestigationCreateRequest(
        claim_text="Oakridge High School will remain closed for two days for preventive pest fumigation.",
        source_origin="Parent Portal Circular",
        origin_type="observed",
        recorded_date="2026-03-10",
        is_demo=True
    )
    inv = create_investigation(req, db_session)
    assert inv.id is not None
    assert len(inv.versions) == 1
    assert inv.versions[0].dna is not None
    assert inv.versions[0].dna["scope"] == "specific"
    assert len(inv.evidence) > 0
    assert inv.verdict is not None

    inv_id = inv.id

    # 2. Add mutated Version 2
    v2_req = AddVersionRequest(
        claim_text="All schools in the district are closed until further notice due to health hazards.",
        source_origin="WhatsApp Forward",
        origin_type="user_submitted",
        recorded_date="2026-03-12"
    )
    inv_v2 = add_claim_version(inv_id, v2_req, db_session)
    assert len(inv_v2.versions) == 2
    assert inv_v2.versions[1].changes_from_previous is not None
    assert inv_v2.versions[1].changes_from_previous["has_mutation"] is True
    assert inv_v2.versions[1].changes_from_previous["scope_change"]["direction"] == "expanded"

    # 3. Fetch by ID
    fetched = get_investigation(inv_id, db_session)
    assert fetched.id == inv_id
    assert len(fetched.versions) == 2

    # 4. List investigations
    all_invs = list_investigations(db=db_session)
    assert any(i.id == inv_id for i in all_invs)

def test_investigation_not_found_handling(db_session):
    with pytest.raises(HTTPException) as exc:
        get_investigation("non-existent-uuid", db_session)
    assert exc.value.status_code == 404

def test_demos_loading_and_seeding(db_session):
    demos = list_demonstrations()
    assert len(demos) == 3
    assert all(d["is_demo"] is True for d in demos)
    
    # Load Demo 1
    demo1 = get_demo_detail("demo-1", db_session)
    assert demo1.demo_id == "demo-1"
    assert len(demo1.versions) == 3
    assert len(demo1.evidence) == 3

def test_compare_claims_direct():
    req = CompareClaimsRequest(
        original_text="One school closed for one day.",
        modified_text="All schools across the state are closed forever."
    )
    res = compare_claim_versions(req)
    assert res.has_mutation is True
    assert res.scope_change["direction"] == "expanded"
    assert len(res.diff_tokens) > 0

def test_claim_dna_empty_text():
    with pytest.raises(HTTPException) as exc:
        get_claim_dna({"text": ""})
    assert exc.value.status_code == 400
