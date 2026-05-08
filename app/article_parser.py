import requests
from bs4 import BeautifulSoup
from newspaper import Article
from app.utils import logger

class ArticleParser:
    @staticmethod
    def parse(url: str) -> dict:
        """
        Parses an article using newspaper3k, with a BS4 fallback.
        Returns a dict containing text, top_image, authors, and publish_date.
        """
        result = {
            "text": "",
            "top_image": "",
            "authors": [],
            "publish_date": None,
            "success": False
        }
        
        try:
            # Attempt newspaper3k first
            article = Article(url, keep_article_html=False)
            article.download()
            article.parse()
            
            if len(article.text.strip()) > 100:
                result["text"] = article.text.strip()
                result["top_image"] = article.top_image
                result["authors"] = article.authors
                result["publish_date"] = article.publish_date
                result["success"] = True
                return result
            else:
                logger.warning(f"newspaper3k extracted very little text for {url}. Falling back to BS4.")
        except Exception as e:
            logger.warning(f"newspaper3k failed for {url}: {e}. Falling back to BS4.")

        # Fallback to BeautifulSoup
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove scripts and styles
            for script in soup(["script", "style", "noscript", "header", "footer", "nav"]):
                script.decompose()
                
            # Try to find article body
            paragraphs = soup.find_all('p')
            text = '\n'.join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20])
            
            if len(text) > 100:
                result["text"] = text
                
                # Attempt to find an og:image
                og_image = soup.find('meta', property='og:image')
                if og_image and og_image.get('content'):
                    result["top_image"] = og_image['content']
                
                result["success"] = True
            else:
                logger.warning(f"BS4 also failed to extract meaningful text for {url}.")
                
        except Exception as e:
            logger.error(f"BS4 parsing failed for {url}: {e}")
            
        return result

article_parser = ArticleParser()
