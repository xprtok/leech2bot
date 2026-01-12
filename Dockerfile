# Use Python 3.10 to prevent 'asyncio' attribute errors found in 3.11+
FROM python:3.10-slim-bookworm

# Set the working directory
WORKDIR /usr/src/app

# Install system dependencies
# - ffmpeg: Required for merging video and audio streams
# - build-essential/python3-dev: Required for tgcrypto and pycryptodomex
# - git: Required to install specialized plugins from GitHub
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    ffmpeg \
    aria2 \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create a downloads folder for the bot
RUN mkdir -p /usr/src/app/downloads && chmod 777 /usr/src/app/downloads

# Copy requirements first to leverage Docker's build cache
COPY requirements.txt .

# Upgrade pip and install core dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- FIX: Install Hanime Plugin directly from GitHub ---
# This bypasses 'No matching distribution' errors on PyPI
RUN pip install --no-cache-dir git+https://github.com/cynthia2006/hanime-plugin.git

# Copy the rest of your application code
COPY . .

# Start the bot
CMD ["python3", "bot.py"]
