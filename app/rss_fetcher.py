import feedparser
from app.config import Config
from app.utils import logger
from datetime import datetime

class RSSFetcher:
    @staticmethod
    def fetch_feeds() -> list[dict]:
        """Fetches the latest articles from all configured RSS feeds."""
        all_articles = []
        for source, url in Config.NEWS_SITES_RSS.items():
            logger.info(f"Fetching RSS feed for {source}: {url}")
            try:
                feed = feedparser.parse(url)
                if not feed.entries:
                    logger.warning(f"No entries found for {source}")
                    continue
                
                # Limit the number of entries
                entries = feed.entries[:Config.MAX_ARTICLES_PER_SOURCE]
                for entry in entries:
                    article_data = {
                        "source": source,
                        "title": entry.get("title", "").strip(),
                        "link": entry.get("link", "").strip(),
                        "published": entry.get("published", datetime.now().isoformat())
                    }
                    if article_data["title"] and article_data["link"]:
                        all_articles.append(article_data)
            except Exception as e:
                logger.error(f"Failed to fetch or parse feed {source}: {e}")
                
        return all_articles

rss_fetcher = RSSFetcher()
