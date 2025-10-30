from sentence_transformers import SentenceTransformer
from typing import List
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating embeddings with Persian support"""

    def __init__(self, model_name: str):
        logger.info(f"Loading embedding model: {model_name}")
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        logger.info(f"✅ Embedding model loaded successfully")

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for single text"""
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        logger.info(f"Generating embeddings for {len(texts)} texts")
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True
        )
        return embeddings.tolist()
