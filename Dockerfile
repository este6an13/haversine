# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Install poetry
RUN pip install poetry

# Set working directory
WORKDIR /app

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure poetry to not create virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev

# Copy source code
COPY src/ ./src/

# Set Python path
ENV PYTHONPATH=/app