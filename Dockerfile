# Use a modern, supported Python image (Debian Bookworm)
# This avoids the "404 Not Found" repository errors
FROM python:3.10-slim-bookworm

# Set the working directory inside the container
WORKDIR /usr/src/app

# Set environment variables to prevent Python from writing .pyc files 
# and to ensure logs are sent straight to the terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
# Every command starts with RUN to avoid "unknown instruction" errors
RUN apt-get update && apt-get install -y --no-install-recommends \
    tor \
    aria2 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy your requirements file first to leverage Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Command to run your bot
# Replace 'bot.py' with the actual name of your main script
CMD ["python3", "bot.py"]
