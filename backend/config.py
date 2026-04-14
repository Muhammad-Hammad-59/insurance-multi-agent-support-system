# backend/config.py
import os
from pathlib import Path

class Config:
    # Base directory
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    # Database paths from environment variables (with defaults)
    SQLITE_PATH = os.getenv('SQLITE_PATH', '/app/data/insurance_support.db')
    print(f"SQLITE_PATH set to: {SQLITE_PATH}")
    CHROMA_PATH = os.getenv('CHROMA_PATH', '/app/chroma_db')
    COLLECTION_NAME = "insurance_FAQ_collection"
    # API Keys
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama3-70b-8192')
    
    # CORS settings for production
    
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:80').split(',')
    print(f"CORS_ORIGINS set to: {CORS_ORIGINS}")
    # Environment
    ENV = os.getenv('ENV', 'development')
    DEBUG = ENV == 'development'
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist"""
        # Create directory for SQLite database
        os.makedirs(os.path.dirname(cls.SQLITE_PATH), exist_ok=True)
        
        # Create directory for ChromaDB
        os.makedirs(cls.CHROMA_PATH, exist_ok=True)
        
        # Set permissions
        os.chmod(os.path.dirname(cls.SQLITE_PATH), 0o755)
        os.chmod(cls.CHROMA_PATH, 0o755)