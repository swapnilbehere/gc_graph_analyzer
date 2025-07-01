# app/config.py

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings for the chromatogram analysis app."""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Model Settings
    LLM_MODEL = "gpt-4o-mini"
    LLM_TEMPERATURE = 0
    EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
    
    # File Processing Settings
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # Directory Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    
    # Input/Output Directories
    CDF_FILES_DIR = os.path.join(DATA_DIR, "cdf_files")
    TEMP_UPLOADS_DIR = os.path.join(DATA_DIR, "temp_uploads")
    JSON_OUTPUT_DIR = os.path.join(DATA_DIR, "json_output")
    TXT_OUTPUT_DIR = os.path.join(DATA_DIR, "txt_output")
    KNOWLEDGE_BASE_DIR = os.path.join(DATA_DIR, "knowledge_base")
    
    # Peak Detection Settings
    HEIGHT_PERCENTILE = 95
    PROMINENCE_PERCENTILE = 90
    MIN_PEAK_DISTANCE = 5
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that all required configuration is present."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Create directories if they don't exist
        for dir_path in [cls.CDF_FILES_DIR, cls.TEMP_UPLOADS_DIR, 
                        cls.JSON_OUTPUT_DIR, cls.TXT_OUTPUT_DIR, 
                        cls.KNOWLEDGE_BASE_DIR]:
            os.makedirs(dir_path, exist_ok=True)
        
        return True
    
    @classmethod
    def get_all_settings(cls) -> Dict[str, Any]:
        """Get all configuration settings as a dictionary."""
        return {
            'llm_model': cls.LLM_MODEL,
            'llm_temperature': cls.LLM_TEMPERATURE,
            'embedding_model': cls.EMBEDDING_MODEL,
            'chunk_size': cls.CHUNK_SIZE,
            'chunk_overlap': cls.CHUNK_OVERLAP,
            'height_percentile': cls.HEIGHT_PERCENTILE,
            'prominence_percentile': cls.PROMINENCE_PERCENTILE,
            'min_peak_distance': cls.MIN_PEAK_DISTANCE
        }