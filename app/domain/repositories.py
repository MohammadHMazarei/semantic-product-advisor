from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities import Product, SearchResult


class ProductRepository(ABC):
    """Abstract repository for product operations"""

    @abstractmethod
    async def load_products(self) -> List[Product]:
        """Load all products from data source"""
        pass

    @abstractmethod
    async def search_products(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Search products by semantic similarity"""
        pass

    @abstractmethod
    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        pass
