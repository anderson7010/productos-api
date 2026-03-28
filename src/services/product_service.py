"""Product service layer for business logic and validations."""

from typing import List
from src.models.product import Product, ProductCreate, ProductUpdate, ProductResponse
from src.repositories.product_repository import ProductRepository


class ProductNotFoundError(Exception):
    """Exception raised when a product is not found."""
    
    def __init__(self, product_id: int) -> None:
        """Initialize the exception with product ID.
        
        Args:
            product_id: ID of the product that was not found
        """
        self.product_id = product_id
        super().__init__(f"Product with id {product_id} not found")


class ProductService:
    """Service layer for product business logic."""
    
    def __init__(self, repository: ProductRepository) -> None:
        """Initialize service with repository dependency.
        
        Args:
            repository: Product repository instance
        """
        self.repository = repository
    
    def create_product(self, product_data: ProductCreate) -> ProductResponse:
        """Create a new product.
        
        Args:
            product_data: Product creation data
            
        Returns:
            Created product response
        """
        created_product = self.repository.create(product_data)
        return self._product_to_response(created_product)
    
    def get_product(self, product_id: int) -> ProductResponse:
        """Get product by ID.
        
        Args:
            product_id: Product ID to retrieve
            
        Returns:
            Product response
            
        Raises:
            ProductNotFoundError: If product is not found
        """
        product = self.repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(product_id)
        
        return self._product_to_response(product)
    
    def get_all_products(self) -> List[ProductResponse]:
        """Get all products.
        
        Returns:
            List of all product responses
        """
        products = self.repository.get_all()
        return [self._product_to_response(product) for product in products]
    
    def update_product(self, product_id: int, update_data: ProductUpdate) -> ProductResponse:
        """Update an existing product.
        
        Args:
            product_id: ID of product to update
            update_data: Product update data
            
        Returns:
            Updated product response
            
        Raises:
            ProductNotFoundError: If product is not found
        """
        updated_product = self.repository.update(product_id, update_data)
        if updated_product is None:
            raise ProductNotFoundError(product_id)
        
        return self._product_to_response(updated_product)
    
    def delete_product(self, product_id: int) -> bool:
        """Delete a product by ID.
        
        Args:
            product_id: ID of product to delete
            
        Returns:
            True if product was deleted
            
        Raises:
            ProductNotFoundError: If product is not found
        """
        deleted = self.repository.delete(product_id)
        if not deleted:
            raise ProductNotFoundError(product_id)
        
        return True
    
    def _product_to_response(self, product: Product) -> ProductResponse:
        """Convert Product model to ProductResponse.
        
        Args:
            product: Product model instance
            
        Returns:
            ProductResponse instance
        """
        return ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock
        )