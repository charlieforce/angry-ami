"""
Utility functions for Angry Ami
"""
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_logging():
    """Configure logging for Ami"""
    log_path = os.getenv('LOG_FILE_PATH', './logs/ami.log')
    
    # Create logs directory if it doesn't exist
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=os.getenv('HERMES_LOG_LEVEL', 'INFO'),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('AmiAgent')

def get_config(key, default=None):
    """Get configuration value from .env"""
    return os.getenv(key, default)

def ensure_directories():
    """Ensure all required directories exist"""
    directories = [
        './data/knowledge_bases',
        './data/learning',
        './data/conversations',
        './data/photos',
        './logs',
        './config'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

logger = setup_logging()
