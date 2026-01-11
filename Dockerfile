# Use an official lightweight Python image
FROM python:3.10-slim-buster

# Install system dependencies
# aria2: for torrents and direct links
# tor: for .onion link support
# curl/wget: for general networking
RUN apt-get update && apt-get install -y \
    aria2 \
    tor \
    curl \
    wget \
    &> /dev/null && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot script into the container
COPY . .

# Expose Tor proxy port (optional, for internal routing)
EXPOSE 9050

# Start the Tor service and then the Bot
CMD service tor start && python3 bot.py
