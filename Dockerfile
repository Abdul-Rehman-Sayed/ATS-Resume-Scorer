FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        libmagic1 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libgdk-pixbuf-2.0-0 \
        libffi-dev \
        libcairo2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt \
    && python -m spacy download en_core_web_sm

COPY backend ./backend

ENV PORT=7860
EXPOSE 7860
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-7860}"]
