# Use Python 3.10 to avoid asyncio and header compatibility issues
FROM python:3.10-slim-bookworm

WORKDIR /usr/src/app

# Install system dependencies + headers needed for C-extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install the specialized hanime plugin directly from source
RUN pip install --no-cache-dir git+https://github.com/cynthia2006/hanime-plugin.git

# Copy the rest of the code
COPY . .

# Start the bot
CMD ["python3", "bot.py"]
