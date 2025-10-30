from functools import lru_cache
from app.core.config import get_settings, Settings
from app.infrastructure.embeddings import EmbeddingService
from app.infrastructure.vector_store import ChromaProductRepository
from app.application.services import ProductSearchService
import logging

logger = logging.getLogger(__name__)

# Singletons
_embedding_service = None
_product_repository = None


def get_embedding_service() -> EmbeddingService:
    """Get or create embedding service singleton"""
    global _embedding_service
    if _embedding_service is None:
        settings = get_settings()
        logger.info(f"Initializing EmbeddingService with model: {settings.EMBEDDING_MODEL_NAME}")
        _embedding_service = EmbeddingService(settings.EMBEDDING_MODEL_NAME)
    return _embedding_service


def get_product_repository() -> ChromaProductRepository:
    """Get or create product repository singleton"""
    global _product_repository
    if _product_repository is None:
        settings = get_settings()
        embedding_service = get_embedding_service()
        logger.info("Initializing ChromaProductRepository")
        _product_repository = ChromaProductRepository(
            embedding_service=embedding_service,
            settings=settings
        )
    return _product_repository


def get_product_search_service() -> ProductSearchService:
    """Get product search service"""
    repository = get_product_repository()
    settings = get_settings()
    return ProductSearchService(repository, settings)
