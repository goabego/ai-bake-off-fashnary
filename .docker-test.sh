#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting Docker test process..."

# Build the Docker image
echo "📦 Building Docker image..."
docker build --platform linux/amd64 -t backend:latest -f backend/Dockerfile .

# Run the Docker container
echo "🚀 Running Docker container..."
docker run -p 8080:8080 backend:latest