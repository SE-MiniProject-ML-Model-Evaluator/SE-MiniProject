# Web Based ML Model Evaluator - application image (US-23, NFR-08)
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_DEBUG=False \
    MLME_MEDIA_ROOT=/data/media \
    MLME_DB_PATH=/data/db.sqlite3

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt gunicorn==23.0.0

COPY . .
RUN chmod +x deploy/entrypoint.sh \
    && useradd --create-home --uid 1000 mlme \
    && mkdir -p /data/media /app/staticfiles \
    && chown -R mlme:mlme /data /app/staticfiles

USER mlme
EXPOSE 8000
ENTRYPOINT ["deploy/entrypoint.sh"]
