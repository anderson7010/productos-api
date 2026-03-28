"""Product router with REST API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.product import ProductCreate, ProductUpdate, ProductResponse
from src.repositories.product_repository import ProductRepository
from src.services.product_service import ProductService, ProductNotFoundError

router = APIRouter(prefix="/products", tags=["products"])


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    """Dependency to get ProductService instance.
    
    Args:
        db: Database session
        
    Returns:
        ProductService instance
    """
    repository = ProductRepository(db)
    return ProductService(repository)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    service: ProductService = Depends(get_product_service)
) -> ProductResponse:
    """Create a new product.
    
    Args:
        product_data: Product creation data
        service: Product service instance
        
    Returns:
        Created product response
    """
    return service.create_product(product_data)


@router.get("/", response_model=List[ProductResponse])
def get_all_products(
    service: ProductService = Depends(get_product_service)
) -> List[ProductResponse]:
    """Get all products.
    
    Args:
        service: Product service instance
        
    Returns:
        List of all products
    """
    return service.get_all_products()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
) -> ProductResponse:
    """Get product by ID.
    
    Args:
        product_id: Product ID to retrieve
        service: Product service instance
        
    Returns:
        Product response
        
    Raises:
        HTTPException: 404 if product not found
    """
    try:
        return service.get_product(product_id)
    except ProductNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {e.product_id} not found"
        )


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    update_data: ProductUpdate,
    service: ProductService = Depends(get_product_service)
) -> ProductResponse:
    """Update an existing product.
    
    Args:
        product_id: ID of product to update
        update_data: Product update data
        service: Product service instance
        
    Returns:
        Updated product response
        
    Raises:
        HTTPException: 404 if product not found
    """
    try:
        return service.update_product(product_id, update_data)
    except ProductNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {e.product_id} not found"
        )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
) -> None:
    """Delete a product by ID.
    
    Args:
        product_id: ID of product to delete
        service: Product service instance
        
    Raises:
        HTTPException: 404 if product not found
    """
    try:
        service.delete_product(product_id)
    except ProductNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {e.product_id} not found"
        )