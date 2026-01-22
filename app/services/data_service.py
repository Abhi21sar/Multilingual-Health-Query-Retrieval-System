import pandas as pd
import numpy as np
import os
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.logging import logger

class DataManager:
    _instance = None
    
    def __init__(self):
        self.raw_data: Optional[pd.DataFrame] = None
        self.corpus_embeddings: Optional[np.ndarray] = None
        self.load_data()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load_data(self):
        """Loads the dataset and embeddings into memory."""
        try:
            logger.info(f"Loading data from {settings.DATA_FILE}...")
            if not os.path.exists(settings.DATA_FILE):
                raise FileNotFoundError(f"Data file not found: {settings.DATA_FILE}")
                
            self.raw_data = pd.read_parquet(settings.DATA_FILE)
            
            logger.info(f"Loading embeddings from {settings.EMBEDDINGS_FILE}...")
            if not os.path.exists(settings.EMBEDDINGS_FILE):
                raise FileNotFoundError(f"Embeddings file not found: {settings.EMBEDDINGS_FILE}")
                
            self.corpus_embeddings = np.load(settings.EMBEDDINGS_FILE)
            logger.info("Data loaded successfully.")
            
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            raise e

    def get_document_by_index(self, idx: int) -> Dict[str, Any]:
        """Retrieves a single document by its index."""
        if self.raw_data is None:
            raise RuntimeError("Data not loaded")
        return self.raw_data.iloc[idx].to_dict()

    def get_embeddings(self) -> np.ndarray:
        if self.corpus_embeddings is None:
            raise RuntimeError("Embeddings not loaded")
        return self.corpus_embeddings
