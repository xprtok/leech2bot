# Use a stable Python 3.10 image
FROM python:3.10-slim-bookworm

# Install dependencies including the specific hanime plugin
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir git+https://github.com/cynthia2006/hanime-plugin.git
    
# Set working directory
WORKDIR /usr/src/app

# Install system dependencies (required for tgcrypto and other bot features)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    tor \
    aria2 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# --- FIX: Explicitly install dependencies ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Start the bot
CMD ["python3", "bot.py"]
