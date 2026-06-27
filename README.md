# ATS Resume Scorer

A web app that parses a resume, scores it against ATS (Applicant Tracking System) criteria and an optional job description, and produces a downloadable PDF report.

## Problem

Most resumes are screened by automated ATS software before a human ever sees them, and candidates rarely know *why* theirs gets filtered out. Online "ATS checkers" are usually generic keyword counters that miss the real signals: whether claimed skills are actually backed by projects, whether keywords from a target job description appear meaningfully, and whether the document is structured for parser-friendly extraction. ATS Resume Scorer combines a structured LLM-based resume parser, semantic skill validation, and a weighted multi-dimensional scorer to give candidates a concrete 0–100 score plus prioritized, actionable feedback — exported as a clean PDF report.

## Features

- Resume parsing for both PDF and DOCX, with hyperlink recovery and resilient fallback (pdfplumber → PyPDF2)
- LLM-based structured extraction (Groq Llama-3.3-70B) into a strict JSON schema with retry-on-bad-JSON
- Skill validation engine — cross-checks each claimed skill against the candidate's projects and experience using semantic embeddings
- Hybrid job-description matching — fuzzy keyword overlap (rapidfuzz) + transformer semantic similarity (all-MiniLM-L6-v2), 0.6 / 0.4 weighted
- spaCy-powered skills-gap analysis identifying missing skills from the JD
- Weighted multi-dimensional scoring across 5 ATS factors (formatting, keywords, content, skill validation, ATS compatibility)
- Downloadable PDF reports via Jinja2 + WeasyPrint
- Supabase-backed authentication (email/password + Google OAuth) with per-user history
- 5 MB upload cap, MIME validation, and explicit rejection of legacy `.doc` files

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend API | FastAPI · Uvicorn · Pydantic |
| LLM | Groq API · Llama-3.3-70B |
| NLP | spaCy (`en_core_web_md`) |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Fuzzy Matching | rapidfuzz |
| File Parsing | pdfplumber · PyPDF2 · python-docx · python-magic |
| PDF Reports | Jinja2 · WeasyPrint |
| Auth & Storage | Supabase (PostgreSQL) · PyJWT |
| Deployment | Docker (python:3.11-slim) |

## How It Works

1. **Sign in** — User authenticates via the Streamlit frontend using Supabase (email/password or Google OAuth).
2. **Upload** — User uploads a resume (PDF or DOCX) and optionally pastes a target job description.
3. **Validation** — Backend checks MIME type via libmagic, enforces the 5 MB cap, and rejects legacy `.doc`.
4. **Text extraction** — pdfplumber extracts text from PDFs (with PyPDF2 fallback); python-docx handles DOCX. Hyperlinks are recovered from PDF annotations and DOCX relationships.
5. **Structured parsing** — Resume text is sent to Groq Llama-3.3-70B, which returns strict JSON: name, skills, experience, projects, education, action verbs, keywords. A JSON-repair retry runs if parsing fails.
6. **Skill validation** — Each extracted skill is compared (exact + semantic via all-MiniLM-L6-v2 cosine similarity) against the candidate's project and experience text. Unbacked skills are flagged.
7. **Multi-dimensional scoring** — Five components are computed and combined with weights:
   - Skills + keywords (40%) — keyword overlap 0.6 + skill validation 0.4
   - Content (30%)
   - Formatting (15%)
   - ATS compatibility (15%)
   Plus rule-based bonuses (perfect grammar, validated skills) and penalties (missing-JD-keyword tiers, location privacy). Final score is clamped to 0–100.
8. **JD matching** (if provided) — Fuzzy keyword overlap (rapidfuzz, threshold 75–80) is combined with semantic cosine similarity at 0.6 / 0.4. spaCy NER + noun-chunk extraction produces a skills-gap report.
9. **Report generation** — Detailed feedback, strengths, and the interpretation string are rendered through Jinja2 HTML sections and converted to a single combined PDF via WeasyPrint.
10. **History** — Each analysis is saved (non-blocking) to the user's Supabase history for future reference.

## Architecture

```
              ┌──────────────────────────────────┐
              │  Streamlit Frontend              │
              │  Supabase Auth (email/Google)    │
              │  Upload · JD paste · Dashboard   │
              └─────────────────┬────────────────┘
                                │  multipart/form-data + JWT
                                ▼
              ┌──────────────────────────────────┐
              │  FastAPI Backend                 │
              │  /api/v1/analyze-resume          │
              │  PyJWT verification (HS256/JWKS) │
              └─────────────────┬────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
 ┌─────────────┐       ┌──────────────────┐    ┌───────────────┐
 │ File Parser │       │ LLM Parser       │    │ Scoring Eng.  │
 │ pdfplumber  │       │ Groq Llama-3.3   │    │ 5 weighted    │
 │ PyPDF2 fb   │       │ → strict JSON    │    │ dimensions    │
 │ python-docx │       │   (retry on err) │    │ bonus/penalty │
 │ libmagic    │       └────────┬─────────┘    └───────┬───────┘
 └─────────────┘                │                      │
                                ▼                      ▼
                       ┌──────────────────┐  ┌──────────────────┐
                       │ Skill Validation │  │ JD Matching      │
                       │ MiniLM-L6 cosine │  │ rapidfuzz 0.6 +  │
                       │ vs projects/exp  │  │ MiniLM 0.4       │
                       └────────┬─────────┘  │ spaCy skills-gap │
                                │            └────────┬─────────┘
                                └────────────┬───────┘
                                             ▼
                                  ┌──────────────────────┐
                                  │ Jinja2 + WeasyPrint  │
                                  │ → Combined PDF       │
                                  └──────────┬───────────┘
                                             ▼
                                  ┌──────────────────────┐
                                  │ Supabase (Postgres)  │
                                  │ users · history      │
                                  └──────────────────────┘
```

## Setup

### Backend

```bash
git clone https://github.com/Abdul-Rehman-Sayed/ats-resume-scorer.git
cd ats-resume-scorer/backend

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt
python -m spacy download en_core_web_md

# Environment variables (.env)
# GROQ_API_KEY=your_groq_api_key
# SUPABASE_URL=your_supabase_url
# SUPABASE_JWT_SECRET=your_supabase_jwt_secret

uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd ../frontend
pip install -r requirements.txt

# .streamlit/secrets.toml
# [backend]
# url = "http://localhost:8000"
# [supabase]
# url = "your_supabase_url"
# anon_key = "your_supabase_anon_key"

streamlit run app.py
```

### Docker (backend)

```bash
docker build -t ats-resume-scorer .
docker run -p 8000:8000 --env-file .env ats-resume-scorer
```

> WeasyPrint requires native dependencies (Pango, Cairo, GDK-PixBuf). On Ubuntu: `sudo apt install libpango-1.0-0 libpangoft2-1.0-0`. The Docker image handles this automatically.

## Limitations & Future Work

- **Heuristic scorer, not learned** — The core ATS score is a hand-tuned weighted heuristic (fixed thresholds, weights, and penalty tiers), not a trained model. Planned: collect labeled ground-truth scores and train a calibrated regressor.
- **Research model not in production** — A fine-tuned sentence-transformer (all-mpnet-base-v2 with CosineSimilarity loss) achieved MAE 0.047 in research notebooks (~70% reduction vs base), but the live app currently uses the off-the-shelf all-MiniLM-L6-v2. Planned: integrate the fine-tuned model behind a feature flag once it is re-validated on a larger held-out set.
- **Stubbed grammar & location checks** — The scoring code supports grammar/spelling penalties, "perfect grammar" bonuses, and location-privacy penalties, but the analysis pipeline currently passes default zero-error results, so these branches never trigger live. Planned: wire up `language-tool-python` for grammar and a proper location/PII detector.
- **Dataset limitations** — Research training used ~266 cleaned resume–JD pairs, which is small and partly templated. Planned: expand and diversify the dataset with real-world anonymized pairs.
- **LLM dependency** — All structured parsing depends on Groq availability and free-tier limits; on two consecutive bad-JSON returns the request raises. Planned: add a deterministic regex/spaCy fallback parser for graceful degradation.
