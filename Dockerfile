FROM python:3.11-slim

# Install system dependencies required by newspaper3k (lxml, etc)
RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    zlib1g-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data for newspaper3k
RUN python -c "import nltk; nltk.download('punkt')" || echo "NLTK punkt download failed, continuing anyway..."

COPY . .

# Command to run the application
CMD ["python", "-m", "app.main"]
