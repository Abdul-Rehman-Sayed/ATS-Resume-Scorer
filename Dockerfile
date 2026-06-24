# Backend (FastAPI) container — works on Hugging Face Spaces, Render, Railway, Fly.io.
FROM python:3.11-slim

# System libraries the backend needs:
#   libmagic1                  -> python-magic (file-type detection)
#   libpango/cairo/gdk-pixbuf  -> WeasyPrint (PDF report generation)
RUN apt-get update && apt-get install -y --no-install-recommends \
        libmagic1 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libgdk-pixbuf-2.0-0 \
        libffi-dev \
        libcairo2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first (better layer caching), then the spaCy model.
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt \
    && python -m spacy download en_core_web_sm

COPY backend ./backend

# Hugging Face Spaces expects 7860; Render/Railway inject $PORT.
ENV PORT=7860
EXPOSE 7860
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-7860}"]
