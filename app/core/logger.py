import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
from app.core.config import settings

def setup_logging():
    """Centralized logging configuration"""
    
    # Create logs directory if not exists
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Base configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler (rotating logs)
    file_handler = RotatingFileHandler(
        filename=logs_dir / "app.log",
        maxBytes=1024 * 1024 * 5,  # 5 MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(name)-12s: %(levelname)-8s %(message)s'
    ))
    
    # Apply handlers to root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    
    # Development-specific logging
    if settings.ENVIRONMENT == "development":
        root_logger.addHandler(console_handler)
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)
    
    # Special logger for Cloudinary operations
    cloudinary_logger = logging.getLogger("cloudinary")
    cloudinary_logger.setLevel(logging.WARNING)
    
    # SQLAlchemy logging control
    if settings.ENVIRONMENT != "development":
        logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)