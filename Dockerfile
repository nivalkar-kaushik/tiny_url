# --- LINE 1 ---
# FROM: Start from an existing base image from Docker Hub
# python:3.12-slim means Python 3.12 on a stripped-down Debian Linux
# "slim" = smaller image size (no dev tools, docs, etc.)
FROM python:3.12-slim

# --- LINE 2 ---
# ENV: Set environment variables inside the container
# PYTHONDONTWRITEBYTECODE=1 → Python won't create .pyc cache files (keeps image clean)
# PYTHONUNBUFFERED=1 → Python output goes directly to the terminal, not buffered
#   (important so you see logs in real time in Docker)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# --- LINE 3 ---
# WORKDIR: Set the working directory inside the container
# All future commands (COPY, RUN, CMD) happen relative to this path
# /app is the convention — think of it as your project's home inside the container
WORKDIR /app

# --- LINE 4 ---
# COPY just the requirements file FIRST, before copying the rest of the code
# WHY? Docker caches layers. If requirements.txt hasn't changed,
# Docker skips re-running pip install (saves minutes on every rebuild)
# This is called the "dependency layer caching" trick — every professional uses it
COPY requirements.txt .

# --- LINE 5 ---
# RUN: Execute a shell command while building the image
# --no-cache-dir → don't store pip's download cache (keeps image smaller)
# --upgrade pip → ensure pip itself is up to date
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- LINE 6 ---
# COPY everything else into the container
# The dot on the left = everything in your current folder on your laptop
# The dot on the right = /app inside the container (our WORKDIR)
# This runs AFTER pip install, so changing your Python code doesn't
# invalidate the pip cache layer above
COPY . .

# --- LINE 8 ---
# EXPOSE: Document which port the app listens on
# This doesn't actually publish the port — that happens in docker-compose.yml
# It's documentation + a hint to Docker tooling
EXPOSE 8000

# --- LINE 9 ---
# CMD: The default command to run when the container starts
# We use gunicorn instead of runserver for production-like behavior
# "tiny_url.wsgi:application" = the wsgi.py file inside tiny_url/ folder
# --bind 0.0.0.0:8000 = listen on all network interfaces (required in containers)
# --workers 2 = 2 worker processes (handles concurrent requests)
# CMD ["gunicorn", "tiny_url.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
    