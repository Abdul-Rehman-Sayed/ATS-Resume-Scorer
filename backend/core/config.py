import os
from pathlib import Path

# Load backend/.env explicitly (this file is backend/core/config.py, so the
# backend dir is one level up). load_dotenv() with no args relies on caller-frame
# inspection that can fail silently under uvicorn reload, leaving env vars unset.
try:
    from dotenv import load_dotenv

    _ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(_ENV_PATH)
except ImportError:
    pass

# api metadata
APP_TITLE = "ATS RESUME ANALYZER"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "analyse resumes against job description using nlp + ml"

# CORS — origins allowed to call the API. allow_credentials=True forbids "*",
# so we list explicit origins. Override in prod via the ALLOWED_ORIGINS env var
# (comma-separated), e.g. "https://myapp.streamlit.app".
ALLOWED_ORIGINS = [
    o.strip()
    for o in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:8501,http://127.0.0.1:8501",
    ).split(",")
    if o.strip()
]

# file
MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# Supported MIME types and their short names
SUPPORTED_MIME_TYPES = {
    "application/pdf": "pdf",
    "application/msword": "doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
}

SUPPORTED_EXTENSIONS = {".pdf", ".doc", ".docx"}

SPACY_MODEL_PRIMARY = "en_core_web_md"  # better accuracy
SPACY_MODEL_SECONDARY = "en_core_web_sm"
SENTENCE_TRANSFORMER_MODEL = os.getenv("SENTENCE_TRANSFORMER_MODEL", "all-MiniLM-L6-v2")

# Score component weights — this is business logic treated as config
SCORE_WEIGHTS = {
    "formatting": 20,
    "keywords": 25,
    "content": 25,
    "skill_validation": 15,
    "ats_compatibility": 15,
}

JD_KEYWORD_WEIGHT = 0.6
JD_SEMANTIC_WEIGHT = 0.4

def _normalize_supabase_url(url: str) -> str:
    """Return the Supabase project base URL.

    The SDK and our REST/JWKS calls append the path themselves, so an accidental
    trailing "/rest/v1" or "/auth/v1" (a common copy-paste mistake) would produce
    doubled paths like ``/rest/v1/rest/v1/...``. Strip it defensively.
    """
    url = url.strip().rstrip("/")
    for suffix in ("/rest/v1", "/auth/v1"):
        if url.endswith(suffix):
            url = url[: -len(suffix)]
    return url.rstrip("/")


SUPABASE_URL = _normalize_supabase_url(os.getenv("SUPABASE_URL", ""))
# service_role key for backend DB writes. NOTE: if a public *anon* key is used
# here instead, Row Level Security MUST be enabled on the `analyses` table or it
# becomes world-readable/writable with that public key.
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
SUPABASE_ANON_KEY = os.getenv(
    "SUPABASE_ANON_KEY", ""
)  # public anon — frontend auth calls
SUPABASE_JWT_SECRET = os.getenv(
    "SUPABASE_JWT_SECRET", ""
)  # used by backend to verify access tokens
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
