import os
import sys

# Ensure workspace root is always in sys.path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_root_dir = os.path.abspath(os.path.join(_current_dir, "..", ".."))
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.database import init_db, SessionLocal
from backend.app.routers import investigations, claims, demos
from backend.app.services.demo_data import DEMO_INVESTIGATIONS, build_demo_investigation
from backend.app.models.investigation import Investigation, ClaimVersion, EvidenceRecord
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("evolution_tracker")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes tables and seeds initial demo investigations."""
    logger.info("Initializing SQLite database...")
    init_db()
    
    # Auto-seed demos if database is fresh
    db = SessionLocal()
    try:
        count = db.query(Investigation).filter(Investigation.is_demo == True).count()
        if count == 0:
            logger.info("Fresh database detected. Auto-seeding 3 prepared demonstration investigations...")
            for raw_demo in DEMO_INVESTIGATIONS:
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
            logger.info("Successfully seeded all 3 demonstration investigations.")
    except Exception as e:
        logger.error(f"Error seeding demo investigations: {e}")
        db.rollback()
    finally:
        db.close()
    yield

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Automated FactChecking & Misinformation Platform — Don't just verify the claim. Track how it changed.",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows local frontend on any port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(investigations.router)
app.include_router(claims.router)
app.include_router(demos.router)

@app.get("/api/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "mode": "live-search-enabled" if bool(settings.TAVILY_API_KEY) else "offline-ready / demo-ready",
        "live_search_configured": bool(settings.TAVILY_API_KEY),
        "ai_configured": bool(settings.GEMINI_API_KEY),
        "tagline": "VERIFY BEFORE YOU SHARE."
    }
