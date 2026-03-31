# ── Backend Dockerfile ──────────────────────────────────────────────
# Python 3.11 slim base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend source
COPY . .

# Flask will listen on 5000
EXPOSE 5000

# Use gunicorn for production; falls back to flask dev server if not installed
CMD ["python", "app.py"]
