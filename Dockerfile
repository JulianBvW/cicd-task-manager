# Use a lightweight base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ src/

# Expose Flask port
EXPOSE 5000

# Run application
CMD ["python", "src/app.py"]
