from fastapi import APIRouter, Depends, HTTPException
import logging

from app.application.dtos import (
    ProductSearchRequestDTO,
    ProductSearchResponseDTO,
)
from app.application.services import ProductSearchService
from app.core.dependencies import get_product_search_service
from app.core.config import get_settings, Settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "/search",
    response_model=ProductSearchResponseDTO,
    summary="search products",
    description="Semantic search in digital marketing products"
)
async def search_products(
        request: ProductSearchRequestDTO,
        service: ProductSearchService = Depends(get_product_search_service),
):
    try:
        results = await service.search_products(request)
        return results
    except Exception as e:
        logger.error(f"Error in search: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error occurred in search: {str(e)}"
        )


@router.get(
    "/health",
    summary="Checking the health of the search system"
)
async def health_check(
        settings: Settings = Depends(get_settings)
):
    """Check the status of the search system and settings"""
    return {
        "status": "healthy",
        "message": "The search system is ready",
        "config": {
            "embedding_model": settings.EMBEDDING_MODEL_NAME,
            "collection_name": settings.COLLECTION_NAME,
            "default_top_k": settings.DEFAULT_SEARCH_TOP_K,
            "max_top_k": settings.MAX_SEARCH_TOP_K,
            "min_relevance_score": settings.MIN_RELEVANCE_SCORE
        }
    }


@router.get(
    "/stats",
    summary="Product statistics"
)
async def get_stats(
        service: ProductSearchService = Depends(get_product_search_service)
):
    """Get statistics on indexed products"""
    try:
        repo = service.repository
        total_products = len(repo._products_cache)
        indexed_count = repo.collection.count()

        return {
            "total_products": total_products,
            "indexed_documents": indexed_count,
            "status": "synced" if total_products == indexed_count else "out_of_sync"
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error in receiving product statistics: {str(e)}"
        )
