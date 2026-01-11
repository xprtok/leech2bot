# Use a slim python image
FROM python:3.10-slim-buster

# Install system dependencies (Aria2, Tor, etc.)
RUN apt-get update && apt-get install -y \
    aria2 \
    tor \
    &> /dev/null && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN useradd -m botuser
WORKDIR /home/botuser

# Create a virtual environment
RUN python -m venv /home/botuser/venv
ENV PATH="/home/botuser/venv/bin:$PATH"

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Change ownership to the non-root user
RUN chown -R botuser:botuser /home/botuser
USER botuser

# Start Tor and the Bot
# Note: Since we are non-root, we start tor as a background process manually
CMD tor & ["python3", "bot.py"]


