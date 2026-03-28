"""Product models and schemas for the API."""

from decimal import Decimal
from typing import Optional
from sqlalchemy import Column, Integer, String, Numeric, Text
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field, field_serializer

Base = declarative_base()


class Product(Base):
    """SQLAlchemy Product model."""
    
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)


class ProductCreate(BaseModel):
    """Schema for creating a new product."""
    
    name: str = Field(..., min_length=1, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: Decimal = Field(..., gt=0, description="Product price")
    stock: int = Field(..., ge=0, description="Product stock quantity")


class ProductUpdate(BaseModel):
    """Schema for updating an existing product."""
    
    name: Optional[str] = Field(None, min_length=1, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: Optional[Decimal] = Field(None, gt=0, description="Product price")
    stock: Optional[int] = Field(None, ge=0, description="Product stock quantity")


class ProductResponse(BaseModel):
    """Schema for product response."""
    
    id: int = Field(..., description="Product ID")
    name: str = Field(..., description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: Decimal = Field(..., description="Product price")
    stock: int = Field(..., description="Product stock quantity")
    
    @field_serializer('price')
    def serialize_price(self, value: Decimal) -> str:
        """Serialize price to string with consistent formatting."""
        # Format to remove trailing zeros and ensure consistent decimal places
        formatted = f"{value:.2f}"
        # Remove trailing zero if it's a whole number with .00
        if formatted.endswith('.00'):
            return formatted[:-1]  # Keep one zero: 50.00 -> 50.0
        return formatted
    
    class Config:
        from_attributes = True