# ATS Resume Scorer

Analyze a resume against ATS (Applicant Tracking System) criteria and an optional
job description. The app parses the resume, scores it across five dimensions,
validates claimed skills against projects and experience, compares it to a job
description, and produces a downloadable PDF report.

## Stack

- **Backend:** FastAPI, spaCy, sentence-transformers, Groq (LLM parsing), WeasyPrint (PDF)
- **Frontend:** Streamlit
- **Auth + storage:** Supabase (email/password + Google OAuth, history saved per user)

## Project layout

```
backend/    FastAPI service (parsing, scoring, PDF, auth, history)
frontend/   Streamlit app (landing, auth, analyzer, history, resources)
notebooks/  Exploratory ML research (not used by the running app)
Dockerfile  Container for the backend
```

## Local setup

Backend:

```bash
cd backend
python -m venv venv
venv/Scripts/activate            # Windows
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Copy `backend/.env.example` to `backend/.env` and fill in your keys, then from the
project root:

```bash
python -m backend.main
```

Frontend (second terminal):

```bash
cd frontend
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
```

Copy `frontend/.env.example` to `frontend/.env`, then from the project root:

```bash
streamlit run frontend/streamlit_app.py
```

The app runs at http://localhost:8501 and talks to the backend at http://localhost:8000.

## Configuration

Backend reads `backend/.env`; the frontend reads `frontend/.env` (or Streamlit
secrets in deployment). See the `.env.example` files for the full list of variables.

## Notes

- PDF generation needs the system graphics libraries (GTK/Pango on Windows, or the
  packages in the `Dockerfile` on Linux). Everything else works without them.
- The `notebooks/` directory holds earlier ML experiments and is independent of the
  production scoring pipeline.
