import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
    NVIDIA_API_BASE = "https://integrate.api.nvidia.com/v1"
    MODEL_NAME = "meta/llama-3.3-70b-instruct"

    R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
    R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
    R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")
    R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
    R2_PUBLIC_URL = os.getenv("R2_PUBLIC_URL")
    R2_ENDPOINT = os.getenv("R2_ENDPOINT")

    FIREBASE_SERVICE_ACCOUNT = os.getenv("FIREBASE_SERVICE_ACCOUNT", "service-account.json")
    FIREBASE_SERVICE_ACCOUNT_JSON = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
    FIREBASE_SERVICE_ACCOUNT_BASE64 = os.getenv("FIREBASE_SERVICE_ACCOUNT_BASE64")

    FETCH_INTERVAL_MINUTES = int(os.getenv("FETCH_INTERVAL_MINUTES", "60"))
    MAX_ARTICLES_PER_SOURCE = int(os.getenv("MAX_ARTICLES_PER_SOURCE", "5"))

    NEWS_SITES_RSS = {
        "India Today": "https://www.indiatoday.in/rss/home",
        "Times of India": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
        "NDTV": "https://feeds.feedburner.com/ndtvnews-top-stories",
        "The Hindu": "https://www.thehindu.com/news/national/feeder/default.rss",
        "Indian Express": "https://indianexpress.com/feed/",
        "Hindustan Times": "https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml",
        "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
        "Reuters": "https://feeds.reuters.com/reuters/topNews",
        "CNN": "http://rss.cnn.com/rss/edition.rss",
        "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
        "NYTimes": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "TechCrunch": "https://techcrunch.com/feed/",
        "The Verge": "https://www.theverge.com/rss/index.xml",
        "Wired": "https://www.wired.com/feed/rss",
        "Ars Technica": "http://feeds.arstechnica.com/arstechnica/index"
    }

    CATEGORIES = [
        "Politics", "Technology", "Sports", "Finance", 
        "Entertainment", "World", "Science", "Business", 
        "Cricket", "Hollywood", "Bollywood", "Tollywood"
    ]
