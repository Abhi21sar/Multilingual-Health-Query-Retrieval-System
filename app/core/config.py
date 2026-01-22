from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "MediQuery Pro"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Model Configuration
    MODEL_PATH: str = "Large-Bert"
    FALLBACK_MODEL: str = "paraphrase-multilingual-MiniLM-L12-v2"
    
    # Data Paths
    DATA_FILE: str = "dataAll.parquet"
    EMBEDDINGS_FILE: str = "corpus_embedding.npy"
    
    # Search Configuration
    TOP_K: int = 10
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
