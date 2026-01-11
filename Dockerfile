# Use 3.10 to fix the asyncio.coroutine error
FROM python:3.10-slim-buster

# Install Tor and Aria2
RUN apt-get update && apt-get install -y \
    tor \
    aria2 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Create a script to start both Tor and the Bot
RUN echo "tor & python3 bot.py" > start.sh && chmod +x start.sh

CMD ["./start.sh"]


