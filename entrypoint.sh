#!/bin/sh
# This shebang line tells the OS to use /bin/sh to run this script
# We use sh instead of bash because some minimal images don't have bash

# --- exit immediately if any command fails ---
# Without "set -e", if migrate fails, the script continues and you
# start a broken server. With it, Docker stops and shows you the error.
set -e

echo "Running database migrations..."
python manage.py migrate --noinput
# --noinput means "don't ask me any questions, just run"

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear
# --clear removes the old staticfiles folder before collecting (fresh start)

echo "Starting Gunicorn..."
# "exec" replaces this shell process with gunicorn
# Without exec, the shell script is PID 1 and gunicorn is a child process
# With exec, gunicorn IS PID 1 — Docker signals (Ctrl+C, stop) reach it directly
exec gunicorn tiny_url.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --access-logfile - \
    --error-logfile -
# --access-logfile - and --error-logfile - → send logs to stdout/stderr
# Docker captures stdout/stderr so you can see logs with "docker compose logs"
