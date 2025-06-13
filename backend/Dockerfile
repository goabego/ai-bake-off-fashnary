# --- Stage 1: Builder (for Python dependencies) ---
FROM python:3.11-slim-bookworm AS builder

# Copy your application code from the 'app' directory
COPY . /app
RUN pip install --no-cache-dir -r /app/requirements.txt

RUN mkdir /db
COPY db/ /db/

RUN mkdir /images
COPY images/ /images/

WORKDIR /app

# Expose the port your application listens on (e.g., for a web app)
EXPOSE 8000

# Command to run your application
CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "api:app"]