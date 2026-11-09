#!/bin/sh
# Prepare the database and static files, then start Gunicorn (Design Spec 2.5 deployment view).
set -e
python manage.py migrate --noinput
python manage.py collectstatic --noinput --verbosity 0
exec gunicorn mlme.wsgi:application --bind 0.0.0.0:8000 --workers "${GUNICORN_WORKERS:-2}" --threads 4 --timeout 180
