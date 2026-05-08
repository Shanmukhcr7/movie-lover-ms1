import time
from app.config import Config
from app.utils import logger
from app.rss_fetcher import rss_fetcher
from app.duplicate_checker import duplicate_checker
from app.article_parser import article_parser
from app.ai_writer import ai_writer
from app.category_classifier import category_classifier
from app.r2_uploader import r2_uploader
from app.firebase_client import firebase_client
from app.slug_generator import slug_generator

def process_single_article(article_meta: dict):
    source = article_meta["source"]
    title = article_meta["title"]
    url = article_meta["link"]
    
    logger.info(f"Processing: {title} from {source}")

    # 1. Duplicate check
    norm_title = duplicate_checker.normalize_string(title)
    if duplicate_checker.is_duplicate(url, norm_title):
        logger.info(f"Skipping duplicate: {title}")
        return
        
    # 2. Extract content
    parsed = article_parser.parse(url)
    if not parsed["success"]:
        logger.warning(f"Skipping {title} - failed to extract content")
        return
        
    original_text = parsed["text"]
    original_image = parsed["top_image"]
    author = ", ".join(parsed["authors"]) if parsed["authors"] else source
    
    # 3. AI Rewrite & Classify
    rewrite_result = ai_writer.rewrite_article(title, original_text)
    if not rewrite_result["success"]:
        logger.warning(f"Skipping {title} - AI rewrite failed")
        return
        
    ai_data = rewrite_result["data"]
    seo_title = ai_data.get("seo_title", title)
    summary = ai_data.get("summary", "")
    content = ai_data.get("content", original_text)
    
    # Append Copyright / Original Source Credit
    content += f"\n\n---\n**Disclaimer:** *This article was originally published by {source}. Read the original article [here]({url}).*"

    keywords = ai_data.get("keywords", [])
    
    category = category_classifier.classify(content)
    
    # 4. Upload Image
    final_image_url = r2_uploader.upload_image(original_image, category) if original_image else ""
    
    # 5. Generate Slug
    slug = slug_generator.generate(seo_title)
    
    # 6. Save to Firestore
    doc_data = {
        "title": seo_title,
        "author": author,
        "imageUrl": final_image_url,
        "originalImage": original_image,
        "videoUrl": None,
        "category": category,
        "summary": summary,
        "content": content,
        "type": "news",
        "source": source,
        "sourceUrl": url,
        "seoSlug": slug,
        "keywords": keywords,
        "automated": True,
        "publishedAutomatically": True,
        "isPromotion": False,
        "isWeeklyMagazine": False,
        "views": 0,
        # createdAt and updatedAt are handled by firebase_client
    }
    
    firebase_client.insert_news_document(doc_data)

def run_job():
    logger.info("Starting news fetching cycle...")
    articles = rss_fetcher.fetch_feeds()
    
    logger.info(f"Found {len(articles)} total articles from feeds.")
    
    # 1. Filter out duplicates first
    new_articles = []
    for article in articles:
        norm_title = duplicate_checker.normalize_string(article["title"])
        if not duplicate_checker.is_duplicate(article["link"], norm_title):
            new_articles.append(article)
            
    logger.info(f"Found {len(new_articles)} new, non-duplicate articles.")
    
    if not new_articles:
        logger.info("No new articles to process. Finishing cycle.")
        return
        
    # 2. Use AI to select the top 3 most important news
    logger.info("Using AI to select the top 3 news stories...")
    top_indices = ai_writer.select_top_articles(new_articles, limit=3)
    top_articles = [new_articles[i] for i in top_indices]
    
    logger.info(f"Selected top {len(top_articles)} articles.")
    
    # 3. Process the selected articles
    for article in top_articles:
        try:
            process_single_article(article)
            # Sleep slightly to avoid rate limiting
            time.sleep(2)
        except Exception as e:
            logger.error(f"Unhandled error processing article {article.get('title')}: {e}")
            
    logger.info("Finished news fetching cycle.")

if __name__ == "__main__":
    from app.scheduler import start_scheduler
    start_scheduler()
