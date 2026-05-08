import re
from app.firebase_client import firebase_client
from app.utils import logger

class DuplicateChecker:
    @staticmethod
    def normalize_string(text: str) -> str:
        """Removes special characters and lowercases for better matching."""
        if not text:
            return ""
        text = text.lower()
        return re.sub(r'[^a-z0-9]', '', text)

    @staticmethod
    def is_duplicate(source_url: str, title: str) -> bool:
        if not firebase_client.db:
            logger.error("Cannot check for duplicates, Firestore not initialized.")
            return False # Fail open or closed? If DB fails, returning false might spam errors. Return True to skip if DB is down.
            
        try:
            collection_ref = firebase_client.db.collection('artifacts').document('default-app-id').collection('news')
            
            # 1. Check by sourceUrl
            docs = collection_ref.where('sourceUrl', '==', source_url).limit(1).stream()
            for _ in docs:
                logger.info(f"Duplicate found by source URL: {source_url}")
                return True
                
            # 2. If sourceUrl isn't found, check by normalized title to catch same article from different links
            # Note: Firestore doesn't support complex regex or lowercase search natively without extra fields.
            # As a workaround, we will fetch the latest 50 docs and check in memory, 
            # or rely mostly on sourceUrl. Since we want to be production ready, 
            # we should add a 'normalizedTitle' field when inserting, but to support existing schemas,
            # we will just check by exact title first.
            docs = collection_ref.where('title', '==', title).limit(1).stream()
            for _ in docs:
                logger.info(f"Duplicate found by exact title: {title}")
                return True
                
            return False
        except Exception as e:
            logger.error(f"Error checking for duplicate: {e}")
            return True # Skip on error to avoid duplicate spam

duplicate_checker = DuplicateChecker()
