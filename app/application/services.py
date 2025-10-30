from typing import List
from app.domain.repositories import ProductRepository
from app.application.dtos import (
    ProductSearchRequestDTO,
    ProductSearchResponseDTO,
    SearchResultDTO,
    ProductDTO
)
from app.core.config import Settings
import logging

logger = logging.getLogger(__name__)


class ProductSearchService:
    """Service for product search operations"""

    def __init__(self, repository: ProductRepository, settings: Settings):
        self.repository = repository
        self.settings = settings

    async def search_products(
            self,
            request: ProductSearchRequestDTO
    ) -> ProductSearchResponseDTO:
        """
        Search products using semantic search
        """
        # Use default top_k from settings if not provided
        top_k = request.top_k or self.settings.DEFAULT_SEARCH_TOP_K

        # Ensure top_k doesn't exceed maximum
        top_k = min(top_k, self.settings.MAX_SEARCH_TOP_K)

        logger.info(f"Searching for: '{request.query}' with top_k={top_k}")

        # Perform search
        results = await self.repository.search_products(
            query=request.query,
            top_k=top_k
        )

        # Filter by minimum relevance score
        filtered_results = [
            result for result in results
            if result.relevance_score >= self.settings.MIN_RELEVANCE_SCORE
        ]

        logger.info(
            f"Found {len(filtered_results)} results "
            f"(filtered from {len(results)} by min_score={self.settings.MIN_RELEVANCE_SCORE})"
        )

        # Convert to DTOs
        result_dtos = [
            SearchResultDTO(
                product=ProductDTO.from_entity(result.product),
                relevance_score=round(result.relevance_score, 3)
            )
            for result in filtered_results
        ]

        return ProductSearchResponseDTO(
            query=request.query,
            results=result_dtos,
            total_found=len(result_dtos),
            min_relevance_score=self.settings.MIN_RELEVANCE_SCORE
        )
