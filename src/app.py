"""FastAPI application with product CRUD and search endpoints."""

from fastapi import FastAPI, HTTPException, Query
from typing import Optional

from src.models import ProductCreate, ProductResponse
from src.store import (
    add_product,
    get_product,
    get_all_products,
    search_products_by_name,
)

app = FastAPI(title="Productos API", description="API para gestión y búsqueda de productos")


@app.post("/products", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate) -> ProductResponse:
    """Create a new product.

    Args:
        product: The product data to create.

    Returns:
        The created product with its auto-generated ID.
    """
    return add_product(
        name=product.name,
        price=product.price,
        category=product.category,
    )


@app.get("/products/search", response_model=list[ProductResponse])
def search_products(name: str = Query(..., description="Search query for product name")) -> list[ProductResponse]:
    """Search products by name using case-insensitive substring matching.

    Args:
        name: The search string to match against product names.

    Returns:
        A list of products whose names contain the query substring.

    Raises:
        HTTPException: 400 if the name query is empty or whitespace-only.
    """
    if not name or not name.strip():
        raise HTTPException(
            status_code=400,
            detail="El parámetro 'name' no puede estar vacío",
        )
    return search_products_by_name(name)


@app.get("/products", response_model=list[ProductResponse])
def list_products() -> list[ProductResponse]:
    """List all products in the store.

    Returns:
        A list of all products.
    """
    return get_all_products()


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: int) -> ProductResponse:
    """Retrieve a product by its ID.

    Args:
        product_id: The integer ID of the product.

    Returns:
        The product matching the given ID.

    Raises:
        HTTPException: 404 if the product is not found.
    """
    product = get_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado",
        )
    return product
