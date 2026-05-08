# AI Automated News Publisher

A production-ready Python microservice that automatically fetches trending news from RSS feeds, rewrites and summarizes them using NVIDIA's AI endpoints (OpenAI SDK compatible), uploads images to Cloudflare R2, and stores the final structured documents directly into Firebase Firestore.

## Features
- **RSS Fetching:** Pulls latest articles from multiple trusted news sources.
- **Article Parsing:** Extracts full text and top images using `newspaper3k` (with `BeautifulSoup4` fallback).
- **AI Rewriting:** Uses `meta/llama-3.3-70b-instruct` via NVIDIA API to professionally rewrite, summarize, generate SEO slugs, and classify categories.
- **Image Hosting:** Uploads extracted images to Cloudflare R2 and provides a public CDN URL.
- **Firestore Integration:** Saves fully structured news documents into `artifacts/default-app-id/news`.
- **Duplicate Prevention:** Checks Firestore for existing articles by source URL and normalized title.
- **Automation:** Uses `APScheduler` to run continuously every X minutes.

## Setup & Installation

### 1. Prerequisites
- Python 3.11+
- Firebase Service Account JSON
- Cloudflare R2 Bucket and API Keys
- NVIDIA API Key

### 2. Environment Variables
Copy `.env.example` to `.env` and fill in your details:
```bash
cp .env.example .env
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt')"
```

### 4. Firebase Setup
Place your `service-account.json` in the root of the project. Make sure it matches the `FIREBASE_SERVICE_ACCOUNT` path in your `.env` file.

### 5. Running the Application
```bash
python -m app.main
```

## Deployment

### Using Docker
A `Dockerfile` and `docker-compose.yml` are included.
```bash
docker-compose up -d
```

### Deploying on Railway / Render
1. Connect your GitHub repository.
2. Ensure you add all the Environment Variables from your `.env` file to the platform's secret manager.
3. For the `service-account.json` on platforms like Render or Railway, you can base64 encode the file and inject it as an environment variable, then decode it at runtime, OR use the platform's secret file mounting feature.
4. Set the Start Command to: `python -m app.main`
