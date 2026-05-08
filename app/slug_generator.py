import re
import uuid

class SlugGenerator:
    @staticmethod
    def generate(title: str) -> str:
        """
        Generates an SEO friendly slug from a title.
        Example: "AI Breakthrough in Healthcare!" -> "ai-breakthrough-in-healthcare"
        """
        # Lowercase
        slug = title.lower()
        # Replace non-alphanumeric characters with hyphens
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        # Strip leading/trailing hyphens
        slug = slug.strip('-')
        
        if not slug:
            # Fallback if title has no valid chars
            slug = f"article-{uuid.uuid4().hex[:8]}"
            
        return slug

slug_generator = SlugGenerator()
