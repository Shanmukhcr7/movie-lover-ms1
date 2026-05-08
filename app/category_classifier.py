from openai import OpenAI
from app.config import Config
from app.utils import logger

class CategoryClassifier:
    def __init__(self):
        self.client = OpenAI(
            base_url=Config.NVIDIA_API_BASE,
            api_key=Config.NVIDIA_API_KEY
        )
        self.model = Config.MODEL_NAME

    def classify(self, text: str) -> str:
        """Classifies the text into one of the allowed categories."""
        categories_str = ", ".join(Config.CATEGORIES)
        system_prompt = (
            f"You are a text classification system. Categorize the given text into exactly ONE of the following categories: {categories_str}. "
            "Reply with ONLY the category name and nothing else."
        )

        user_prompt = f"Text to classify: {text[:1000]}"

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=10,
                stream=False
            )
            
            category = completion.choices[0].message.content.strip()
            # Validate
            for valid_cat in Config.CATEGORIES:
                if valid_cat.lower() in category.lower():
                    return valid_cat
            
            logger.warning(f"AI returned invalid category '{category}', defaulting to 'World'")
            return "World"
            
        except Exception as e:
            logger.error(f"AI classification failed: {e}")
            return "World" # Default fallback

category_classifier = CategoryClassifier()
