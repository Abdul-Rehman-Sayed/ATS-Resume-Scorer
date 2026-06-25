import os
from pathlib import Path

try:
    from dotenv import load_dotenv

    _ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(_ENV_PATH)
except ImportError:
    pass

APP_TITLE = "ATS RESUME ANALYZER"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "analyse resumes against job description using nlp + ml"

ALLOWED_ORIGINS = [
    o.strip()
    for o in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:8501,http://127.0.0.1:8501",
    ).split(",")
    if o.strip()
]

MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

SUPPORTED_MIME_TYPES = {
    "application/pdf": "pdf",
    "application/msword": "doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
}

SUPPORTED_EXTENSIONS = {".pdf", ".doc", ".docx"}

SPACY_MODEL_PRIMARY = "en_core_web_md"
SPACY_MODEL_SECONDARY = "en_core_web_sm"
SENTENCE_TRANSFORMER_MODEL = os.getenv("SENTENCE_TRANSFORMER_MODEL", "all-MiniLM-L6-v2")

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
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
SUPABASE_ANON_KEY = os.getenv(
    "SUPABASE_ANON_KEY", ""
)
SUPABASE_JWT_SECRET = os.getenv(
    "SUPABASE_JWT_SECRET", ""
)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
