import json
from openai import OpenAI
from app.config import Config
from app.utils import logger

class AIWriter:
    def __init__(self):
        self.client = OpenAI(
            base_url=Config.NVIDIA_API_BASE,
            api_key=Config.NVIDIA_API_KEY
        )
        self.model = Config.MODEL_NAME

    def rewrite_article(self, original_title: str, original_text: str) -> dict:
        """
        Rewrites the article, generates a summary, an SEO title, and keywords.
        Expects a JSON response from the model.
        """
        system_prompt = (
            "You are a professional news editor. Your task is to rewrite the provided news article to be highly engaging, "
            "objective, and grammatically perfect. Avoid plagiarism by fully rewriting the content. Do not hallucinate or add fake information. "
            "Return the output as a strictly valid JSON object with the following keys:\n"
            "- \"seo_title\": A clickworthy, highly SEO-optimized title (max 60 characters).\n"
            "- \"summary\": A concise summary of the article (1-2 sentences).\n"
            "- \"content\": The full, rewritten article. You MUST use Markdown for great SEO (e.g. use <h2> or <h3> headings, bold important keywords, and use bullet points where appropriate).\n"
            "- \"keywords\": A list of 3-5 relevant keywords.\n"
            "CRITICAL: You must ensure all quotes inside string values are properly escaped (e.g. \\\") so the JSON is completely valid. "
            "Do not include Markdown blocks like ```json in your response. Just the raw JSON object."
        )

        user_prompt = f"Original Title: {original_title}\n\nOriginal Text:\n{original_text[:4000]}" # Limit text to avoid token limits

        for attempt in range(2):
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2,
                    top_p=0.7,
                    max_tokens=1500,
                    response_format={"type": "json_object"},
                    stream=False
                )
                
                response_content = completion.choices[0].message.content.strip()
                
                # Clean up the response if it contains markdown formatting
                if response_content.startswith("```json"):
                    response_content = response_content[7:]
                if response_content.endswith("```"):
                    response_content = response_content[:-3]
                    
                result = json.loads(response_content)
                return {
                    "success": True,
                    "data": result
                }
                
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON from AI response on attempt {attempt + 1}: {e}")
                logger.debug(f"Raw AI response: {response_content}")
                if attempt == 1:
                    return {"success": False, "error": "Invalid JSON response"}
            except Exception as e:
                logger.error(f"AI rewriting failed: {e}")
                return {"success": False, "error": str(e)}

    def select_top_articles(self, articles: list, limit: int = 3) -> list:
        """
        Uses AI to select the top `limit` most important/breaking news articles from a list.
        Expects a list of dictionaries with 'title' and 'source'.
        Returns the indices of the selected articles.
        """
        if len(articles) <= limit:
            return list(range(len(articles)))

        articles_text = ""
        for i, article in enumerate(articles):
            articles_text += f"[{i}] {article['title']} (Source: {article['source']})\n"

        system_prompt = (
            "You are a senior news editor. Your job is to select the most important, trending, and breaking news stories from a list of articles. "
            f"Select exactly {limit} articles. Return your selection as a strictly valid JSON object with a single key 'selected_indices' "
            "which contains an array of the integer indices of your chosen articles. "
            "Do not include Markdown blocks like ```json in your response. Just the raw JSON object."
        )

        user_prompt = f"Please select the top {limit} most important news articles from the following list:\n\n{articles_text}"

        for attempt in range(2):
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.1,
                    max_tokens=150,
                    response_format={"type": "json_object"},
                    stream=False
                )
                
                response_content = completion.choices[0].message.content.strip()
                if response_content.startswith("```json"):
                    response_content = response_content[7:]
                if response_content.endswith("```"):
                    response_content = response_content[:-3]
                    
                result = json.loads(response_content)
                indices = result.get("selected_indices", [])
                
                if isinstance(indices, list) and len(indices) > 0:
                    valid_indices = [idx for idx in indices if isinstance(idx, int) and 0 <= idx < len(articles)]
                    if valid_indices:
                        return valid_indices[:limit]
                
                raise ValueError("AI returned invalid indices structure")
                
            except Exception as e:
                logger.warning(f"Failed to parse AI top selection on attempt {attempt + 1}: {e}")
                
        # Fallback if AI fails: just take the first `limit`
        logger.error("AI top selection failed. Falling back to first few articles.")
        return list(range(min(limit, len(articles))))

ai_writer = AIWriter()
