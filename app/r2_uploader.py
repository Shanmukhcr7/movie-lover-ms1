import uuid
import boto3
import requests
from datetime import datetime
from app.config import Config
from app.utils import logger

class R2Uploader:
    def __init__(self):
        self.s3_client = boto3.client(
            service_name='s3',
            endpoint_url=Config.R2_ENDPOINT,
            aws_access_key_id=Config.R2_ACCESS_KEY,
            aws_secret_access_key=Config.R2_SECRET_KEY,
            region_name='auto'
        )

    def upload_image(self, image_url: str, category: str) -> str:
        """
        Downloads an image from the given URL and uploads it to Cloudflare R2.
        Returns the public URL if successful, otherwise returns the original image_url.
        """
        if not image_url or not Config.R2_ACCESS_KEY:
            return image_url

        try:
            # Download image
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(image_url, headers=headers, stream=True, timeout=10)
            response.raise_for_status()

            # Determine content type and extension
            content_type = response.headers.get('content-type', 'image/jpeg')
            ext = '.jpg'
            if 'png' in content_type:
                ext = '.png'
            elif 'webp' in content_type:
                ext = '.webp'
            elif 'gif' in content_type:
                ext = '.gif'

            # Generate unique filename
            date_str = datetime.now().strftime('%Y-%m')
            safe_category = category.lower().replace(' ', '-')
            filename = f"news/{date_str}/{safe_category}/{uuid.uuid4().hex}{ext}"

            # Upload to R2
            self.s3_client.upload_fileobj(
                response.raw,
                Config.R2_BUCKET_NAME,
                filename,
                ExtraArgs={'ContentType': content_type}
            )

            # Return public URL
            public_url = f"{Config.R2_PUBLIC_URL}/{filename}"
            logger.info(f"Successfully uploaded image to R2: {public_url}")
            return public_url

        except Exception as e:
            logger.error(f"Failed to upload image to R2 ({image_url}): {e}")
            return image_url # Fallback to original URL

r2_uploader = R2Uploader()
