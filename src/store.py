"""In-memory store for products with access and reset functions."""

from __future__ import annotations

from typing import Optional

from src.models import ProductResponse


_products: dict[int, dict] = {}
_counter: int = 0


def get_next_id() -> int:
    """Generate and return the next auto-incremented product ID.

    Returns:
        The next available integer ID, starting from 1.
    """
    global _counter
    _counter += 1
    return _counter


def add_product(name: str, price: float, category: Optional[str] = None) -> ProductResponse:
    """Add a new product to the store.

    Args:
        name: The product name.
        price: The product price (must be > 0).
        category: Optional product category.

    Returns:
        A ProductResponse with the created product data including its generated ID.
    """
    product_id = get_next_id()
    product_data = {
        "id": product_id,
        "name": name,
        "price": price,
        "category": category,
    }
    _products[product_id] = product_data
    return ProductResponse(**product_data)


def get_product(product_id: int) -> Optional[ProductResponse]:
    """Retrieve a product by its ID.

    Args:
        product_id: The integer ID of the product to retrieve.

    Returns:
        A ProductResponse if found, or None if the product does not exist.
    """
    product_data = _products.get(product_id)
    if product_data is None:
        return None
    return ProductResponse(**product_data)


def get_all_products() -> list[ProductResponse]:
    """Return all products in the store.

    Returns:
        A list of ProductResponse objects for every product in the store.
    """
    return [ProductResponse(**data) for data in _products.values()]


def search_products_by_name(query: str) -> list[ProductResponse]:
    """Search products by name using case-insensitive substring matching.

    Args:
        query: The search string to match against product names.
              Leading/trailing whitespace is stripped before matching.

    Returns:
        A list of ProductResponse objects whose names contain the query substring.
    """
    query_lower = query.strip().lower()
    results: list[ProductResponse] = []
    for data in _products.values():
        if query_lower in data["name"].lower():
            results.append(ProductResponse(**data))
    return results


def clear_store() -> None:
    """Reset the store by clearing all products and resetting the ID counter to 0."""
    global _counter
    _products.clear()
    _counter = 0
