"""Pydantic models for Product API request/response schemas."""

from pydantic import BaseModel, Field
from typing import Optional


class ProductCreate(BaseModel):
    """Schema for creating a new product.

    Attributes:
        name: Product name, must be at least 1 character.
        price: Product price, must be greater than 0.
        category: Optional product category.
    """

    name: str = Field(..., min_length=1, description="Product name")
    price: float = Field(..., gt=0, description="Product price, must be > 0")
    category: Optional[str] = Field(default=None, description="Optional product category")


class ProductResponse(BaseModel):
    """Schema for product responses.

    Attributes:
        id: Auto-generated product ID.
        name: Product name.
        price: Product price.
        category: Optional product category.
    """

    id: int
    name: str
    price: float
    category: Optional[str] = None
