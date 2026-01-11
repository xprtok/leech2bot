# Force Python 3.10 to fix the 'asyncio.coroutine' error seen in your logs
FROM python:3.10-slim-buster

# Install necessary system binaries for Tor and Aria2
RUN apt-get update && apt-get install -y \
    tor \
    aria2 \
    curl \
    && rm -rf /var/lib/apt/lists/*

    # Install Tor and Aria2 binaries
RUN apt-get update && apt-get install -y tor aria2 curl && rm -rf /var/lib/apt/lists/*

# Install Tor and Aria2 binaries
RUN apt-get update && apt-get install -y \
    tor \
    aria2 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project files
COPY . .

# Create a small script to run Tor in the background and then start the bot
RUN echo "#!/bin/sh\ntor &\npython3 bot.py" > start.sh && chmod +x start.sh

# Use the script to start the container
CMD [". python3, bot.py"]


