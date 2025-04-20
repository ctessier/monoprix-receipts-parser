# syntax=docker/dockerfile:1

FROM python:3.13-slim

# Install uv
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy the pyproject.toml and optional uv.lock if exists
COPY pyproject.toml .
COPY uv.lock .

# Install dependencies with uv (similar to pip install)
RUN uv pip install --system --no-cache .

# Copy the application source code
COPY src/ src/

# Environment variables
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "src/main.py"]
