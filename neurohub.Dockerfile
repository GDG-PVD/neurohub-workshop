# Dockerfile for NeuroHub Flask Application
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and wheel file
COPY requirements.txt .
COPY agents/a2a_common-0.1.0-py3-none-any.whl ./agents/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the neurohub application
COPY neurohub/ ./neurohub/

# Set working directory to neurohub
WORKDIR /app/neurohub

# Environment variables (will be overridden by Cloud Run)
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# Expose port
EXPOSE 8080

# Run with gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app