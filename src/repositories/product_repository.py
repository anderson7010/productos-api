"""Product repository for database operations."""

from typing import List, Optional
from sqlalchemy.orm import Session

from src.models.product import Product, ProductCreate, ProductUpdate


class ProductRepository:
    """Repository for Product database operations."""
    
    def __init__(self, db: Session) -> None:
        """Initialize repository with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    def create(self, product_data: ProductCreate) -> Product:
        """Create a new product in the database.
        
        Args:
            product_data: Product creation data
            
        Returns:
            Created product instance
        """
        db_product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            stock=product_data.stock
        )
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product
    
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID.
        
        Args:
            product_id: Product ID to search for
            
        Returns:
            Product instance if found, None otherwise
        """
        return self.db.query(Product).filter(Product.id == product_id).first()
    
    def get_all(self) -> List[Product]:
        """Get all products from the database.
        
        Returns:
            List of all products
        """
        return self.db.query(Product).all()
    
    def update(self, product_id: int, update_data: ProductUpdate) -> Optional[Product]:
        """Update an existing product.
        
        Args:
            product_id: ID of product to update
            update_data: Product update data
            
        Returns:
            Updated product instance if found, None otherwise
        """
        db_product = self.get_by_id(product_id)
        if db_product is None:
            return None
        
        # Update only provided fields
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(db_product, field, value)
        
        self.db.commit()
        self.db.refresh(db_product)
        return db_product
    
    def delete(self, product_id: int) -> bool:
        """Delete a product by ID.
        
        Args:
            product_id: ID of product to delete
            
        Returns:
            True if product was deleted, False if not found
        """
        db_product = self.get_by_id(product_id)
        if db_product is None:
            return False
        
        self.db.delete(db_product)
        self.db.commit()
        return True
    
    def exists(self, product_id: int) -> bool:
        """Check if a product exists by ID.
        
        Args:
            product_id: Product ID to check
            
        Returns:
            True if product exists, False otherwise
        """
        return self.db.query(Product).filter(Product.id == product_id).first() is not None
    
    def reset_database(self) -> None:
        """Reset database by deleting all products.
        
        This method is primarily for testing purposes.
        """
        self.db.query(Product).delete()
        self.db.commit()