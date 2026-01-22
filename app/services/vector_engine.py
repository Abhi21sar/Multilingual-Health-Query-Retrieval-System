from sentence_transformers import SentenceTransformer
import scipy.spatial.distance
import numpy as np
import os
from typing import List, Dict, Any, Tuple
from app.core.config import settings
from app.core.logging import logger
from app.services.data_service import DataManager

class VectorEngine:
    _instance = None

    def __init__(self):
        self.embedder = self._load_model()
        self.data_manager = DataManager.get_instance()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_model(self) -> SentenceTransformer:
        """Loads the Sentence Transformer model."""
        if os.path.exists(settings.MODEL_PATH):
            logger.info(f"Loading local model from {settings.MODEL_PATH}...")
            return SentenceTransformer(settings.MODEL_PATH)
        else:
            logger.warning(f"Local model not found. Downloading fallback: {settings.FALLBACK_MODEL}")
            return SentenceTransformer(settings.FALLBACK_MODEL)

    def search(self, query: str, top_k: int = settings.TOP_K) -> List[Dict[str, Any]]:
        """
        Performs a semantic search for the given query.
        Returns a list of top_k results with confidence scores.
        """
        try:
            # 1. Encode the query
            query_embedding = self.embedder.encode(query)
            
            # 2. Get corpus embeddings
            corpus_embeddings = self.data_manager.get_embeddings()
            
            # 3. Calculate Cosine Distances
            # Note: cdist calculates distance. Similarity = 1 - distance.
            distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, "cosine")[0]
            
            # 4. Sort results
            # Create (index, distance) pairs
            results_with_score = zip(range(len(distances)), distances)
            sorted_results = sorted(results_with_score, key=lambda x: x[1])
            
            # 5. Format Output
            output = []
            for idx, distance in sorted_results[0:top_k]:
                doc = self.data_manager.get_document_by_index(idx)
                
                # Convert cosine distance to a confidence percentage
                # Distance ranges from 0 (identical) to 2 (opposite).
                # Similarity = 1 - distance.
                confidence = (1 - distance) * 100
                doc['confidence'] = round(confidence, 2)
                output.append(doc)
                
            return output
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise e
