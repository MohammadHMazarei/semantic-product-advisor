from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class ProductSearchRequestDTO(BaseModel):
    """"DTO for product search request"""
    query: str = Field(
        ...,
        min_length=2,
        max_length=500,
        description="search product in Farsi"
    )
    top_k: Optional[int] = Field(
        default=None,
        ge=1,
        description="number of results (optional)"
    )

    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        """Validate and clean query"""
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "query": "مدیریت اینستاگرام",
                "top_k": 5
            }
        }


class ProductDTO(BaseModel):
    """DTO for product response"""
    id: int
    name: str
    slug: str
    permalink: str
    description_preview: str
    price_display: str

    @classmethod
    def from_entity(cls, product) -> "ProductDTO":
        """Convert domain entity to DTO"""
        import re

        # Clean HTML from description
        clean_desc = re.sub('<[^<]+?>', '', product.description)
        clean_desc = re.sub(r'\s+', ' ', clean_desc).strip()

        # Create preview
        preview = clean_desc[:200] + "..." if len(clean_desc) > 200 else clean_desc

        # Price display (can be enhanced based on actual data)
        price_display = "قیمت: تماس بگیرید"

        return cls(
            id=product.id,
            name=product.name,
            slug=product.slug,
            permalink=product.permalink,
            description_preview=preview,
            price_display=price_display
        )


class SearchResultDTO(BaseModel):
    """DTO for search result"""
    product: ProductDTO
    relevance_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="relevance score (0-1)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "product": {
                    "id": 9177,
                    "name": "مدیریت پیج اینستاگرام (اقتصادی)",
                    "slug": "instagram-page-management-economic",
                    "relevance_score": 0.89
                }
            }
        }


class ProductSearchResponseDTO(BaseModel):
    """DTO for search response"""
    query: str
    results: List[SearchResultDTO]
    total_found: int
    min_relevance_score: float
