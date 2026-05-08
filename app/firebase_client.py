import firebase_admin
from firebase_admin import credentials, firestore
from app.config import Config
from app.utils import logger

class FirebaseClient:
    def __init__(self):
        self.db = None
        self._initialize()

    def _initialize(self):
        if not firebase_admin._apps:
            try:
                if Config.FIREBASE_SERVICE_ACCOUNT_JSON:
                    import json
                    cred_dict = json.loads(Config.FIREBASE_SERVICE_ACCOUNT_JSON)
                    cred = credentials.Certificate(cred_dict)
                else:
                    cred = credentials.Certificate(Config.FIREBASE_SERVICE_ACCOUNT)
                firebase_admin.initialize_app(cred)
                logger.info("Firebase Admin initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize Firebase Admin: {e}")
        
        try:
            self.db = firestore.client()
        except Exception as e:
            logger.error(f"Failed to initialize Firestore client: {e}")

    def insert_news_document(self, data: dict):
        if not self.db:
            logger.error("Firestore client is not initialized.")
            return False
        
        try:
            # Update data with server timestamp
            data["createdAt"] = firestore.SERVER_TIMESTAMP
            data["updatedAt"] = firestore.SERVER_TIMESTAMP
            
            collection_ref = self.db.collection('artifacts').document('default-app-id').collection('news')
            collection_ref.add(data)
            logger.info(f"Successfully inserted article into Firestore: {data.get('title')}")
            return True
        except Exception as e:
            logger.error(f"Failed to insert document into Firestore: {e}")
            return False

firebase_client = FirebaseClient()
