# app/utils/cloudinary_utils.py
import cloudinary
import cloudinary.uploader
import cloudinary.api
from fastapi import HTTPException, status
from urllib.parse import urlparse
from app.core.config import settings
import logging
from typing import Optional

# Configure logger
logger = logging.getLogger(__name__)

# Initialize Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

def upload_to_cloudinary(
    file_content: bytes,
    folder: str = "avatars",
    public_id: Optional[str] = None,
    width: int = 250,
    height: int = 250,
    crop: str = "fill"
) -> str:
    """
    Uploads an image to Cloudinary with automatic resizing
    
    Args:
        file_content: Binary content of the image
        folder: Cloudinary folder to store the image
        public_id: Optional custom public ID
        width: Target width in pixels
        height: Target height in pixels
        crop: Cloudinary crop mode ('fill', 'fit', etc.)
    
    Returns:
        str: Secure URL of the uploaded image
        
    Raises:
        HTTPException: If upload fails
    """
    try:
        result = cloudinary.uploader.upload(
            file_content,
            folder=folder,
            public_id=public_id,
            width=width,
            height=height,
            crop=crop,
            quality="auto",
            format="webp"  # Modern format for better compression
        )
        logger.info(f"Image uploaded to Cloudinary: {result['public_id']}")
        return result["secure_url"]
    except Exception as e:
        logger.error(f"Cloudinary upload failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Image upload failed. Please try another image."
        )

def delete_from_cloudinary(url: str) -> bool:
    """
    Deletes an image from Cloudinary using its URL
    
    Args:
        url: Full Cloudinary URL of the image
        
    Returns:
        bool: True if deletion succeeded, False if no image existed
        
    Raises:
        HTTPException: If deletion fails for existing image
    """
    if not url:
        return False
        
    try:
        public_id = extract_public_id(url)
        if not public_id:
            return False
            
        result = cloudinary.uploader.destroy(public_id)
        if result.get("result") == "ok":
            logger.info(f"Deleted Cloudinary image: {public_id}")
            return True
        else:
            raise Exception(f"Cloudinary deletion failed: {result}")
    except Exception as e:
        logger.error(f"Cloudinary deletion error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Failed to delete existing avatar image"
        )

def extract_public_id(url: str) -> Optional[str]:
    """
    Extracts Cloudinary public ID from a URL
    
    Args:
        url: Cloudinary image URL
        
    Returns:
        str: Public ID if valid URL, None otherwise
    """
    if not url or "cloudinary.com" not in url:
        return None
        
    try:
        path = urlparse(url).path
        parts = path.split('/')
        
        # Handle different URL formats:
        # 1. https://res.cloudinary.com/cloudname/image/upload/v123/public_id.jpg
        # 2. https://res.cloudinary.com/cloudname/image/upload/public_id.jpg
        if "upload" in parts:
            upload_index = parts.index("upload")
            public_id_with_ext = '/'.join(parts[upload_index+2:])
            return public_id_with_ext.split('.')[0]
        return None
    except Exception as e:
        logger.warning(f"Failed to extract public ID from URL: {url} - {str(e)}")
        return None