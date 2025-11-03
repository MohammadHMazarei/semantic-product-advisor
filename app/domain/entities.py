from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Product(BaseModel):
    """Domain entity for Product"""
    id: int
    name: str
    slug: str
    permalink: str
    description: str
    price: str
    date_created: datetime
    status: str

    class Config:
        from_attributes = True


class SearchResult(BaseModel):
    """Domain entity for Search Result"""
    product: Product
    relevance_score: float
    matched_content: str
