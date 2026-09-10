# Use a slim Python image to keep the application image as small as possible.
FROM python:3.12-slim

# Disable .pyc files, enable unbuffered logs, and prevent pip from caching packages.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# All application files and persistent data live under this directory.
WORKDIR /app

# Install runtime libraries required by pygame, Pillow, and scientific Python packages.
# The build tools are needed by packages that compile native extensions during installation.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libglib2.0-0 \
        libgl1 \
        libsm6 \
        libxext6 \
        libxrender1 \
        portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies in a separate layer to improve build-cache reuse.
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the application source code and create directories used by persistent volumes.
COPY . .
RUN mkdir -p /app/data /app/vector_db /app/screenshots /app/generated_images \
    && useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /app

# Run the application as a non-root user.
USER appuser

# Start the interactive TalhaGPT CLI when the container launches.
ENTRYPOINT ["python", "main.py"]
