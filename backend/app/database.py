from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.app.config import settings

connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    # Import models so tables are registered
    from backend.app.models import investigation  # noqa
    Base.metadata.create_all(bind=engine)
    
    # Auto-migrate columns if using SQLite
    try:
        with engine.connect() as conn:
            result = conn.execute(Base.metadata.tables["investigations"].select().limit(0))
    except Exception:
        pass
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            cols = [row[1] for row in conn.execute(text("PRAGMA table_info(investigations)")).fetchall()]
            if cols:
                if "evidence_mode" not in cols:
                    conn.execute(text("ALTER TABLE investigations ADD COLUMN evidence_mode VARCHAR(50) DEFAULT 'offline_demo'"))
                if "confidence" not in cols:
                    conn.execute(text("ALTER TABLE investigations ADD COLUMN confidence VARCHAR(20) DEFAULT 'LOW'"))
                if "analysis_mode" not in cols:
                    conn.execute(text("ALTER TABLE investigations ADD COLUMN analysis_mode VARCHAR(50) DEFAULT 'offline_fallback'"))
                conn.commit()
    except Exception:
        pass
