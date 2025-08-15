# --- Stage 1: Build & Test ---
FROM python:3.11-slim as test

WORKDIR /app

# Copy requirements first
COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy app code
COPY src/ src/
COPY tests/ tests/

# Run lint and tests
RUN flake8 src tests && pytest


# --- Stage 2: Production Image ---
FROM python:3.11-slim as prod

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

# Expose Flask port
EXPOSE 5000

# Run application
CMD ["python", "src/app.py"]
