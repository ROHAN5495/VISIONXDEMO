import os
import sys
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv

# Ensure project root is in sys.path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_root_dir = os.path.abspath(os.path.join(_current_dir, "..", ".."))
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

# Load .env file from root
env_path = os.path.join(_root_dir, ".env")
load_dotenv(dotenv_path=env_path)

db_path = os.path.join(_root_dir, "evolution_tracker.db").replace("\\", "/")

class Settings(BaseModel):
    APP_NAME: str = "Evolution Tracker 2.0"
    APP_VERSION: str = "2.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Database (SQLite with foreign keys enabled, modular for MySQL/PostgreSQL)
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{db_path}")
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    
    # Search APIs (optional)
    SERPAPI_API_KEY: str = os.getenv("SERPAPI_API_KEY", "")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")

    # Optional AI Provider (Google Gemini Developer API)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

settings = Settings()
