FROM python:3.10-slim-bookworm

WORKDIR /usr/src/app

# Install system dependencies + C compilers
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    tor \
    aria2 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Start the bot
CMD ["python3", "bot.py"]
