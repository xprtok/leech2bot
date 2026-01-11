# 1. Use a modern, supported image
FROM python:3.10-slim-bookworm

# 2. Set the working directory
WORKDIR /usr/src/app

# 3. Install system dependencies + Build tools for C-extensions
# Adding build-essential fixes the 'autoconf error'
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    tor \
    aria2 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements and install (Ensure pycryptodome is in here)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your bot code
COPY . .

# 6. Run your bot (Ensure bot.py matches your filename)
CMD ["python3", "bot.py"]
