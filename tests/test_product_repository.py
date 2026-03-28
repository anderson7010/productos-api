import pytest
from decimal import Decimal

from src.models.product import Product, ProductCreate, ProductUpdate
from src.repositories.product_repository import ProductRepository


class TestProductRepository:
    """Test ProductRepository database operations."""
    
    def test_should_create_product(self, db_session):
        """Test creating a new product."""
        repo = ProductRepository(db_session)
        product_data = ProductCreate(
            name="Test Product",
            description="A test product",
            price=Decimal("99.99"),
            stock=10
        )
        
        created_product = repo.create(product_data)
        
        assert created_product.id is not None
        assert created_product.name == "Test Product"
        assert created_product.description == "A test product"
        assert created_product.price == Decimal("99.99")
        assert created_product.stock == 10
    
    def test_should_create_product_without_description(self, db_session):
        """Test creating product without description."""
        repo = ProductRepository(db_session)
        product_data = ProductCreate(
            name="No Description",
            price=Decimal("50.0"),
            stock=5
        )
        
        created_product = repo.create(product_data)
        
        assert created_product.id is not None
        assert created_product.name == "No Description"
        assert created_product.description is None
        assert created_product.price == Decimal("50.0")
        assert created_product.stock == 5
    
    def test_should_get_product_by_id(self, db_session):
        """Test retrieving product by ID."""
        repo = ProductRepository(db_session)
        product_data = ProductCreate(
            name="Findable Product",
            price=Decimal("75.0"),
            stock=3
        )
        created_product = repo.create(product_data)
        
        found_product = repo.get_by_id(created_product.id)
        
        assert found_product is not None
        assert found_product.id == created_product.id
        assert found_product.name == "Findable Product"
        assert found_product.price == Decimal("75.0")
        assert found_product.stock == 3
    
    def test_should_return_none_for_nonexistent_id(self, db_session):
        """Test getting product with non-existent ID returns None."""
        repo = ProductRepository(db_session)
        
        found_product = repo.get_by_id(999)
        
        assert found_product is None
    
    def test_should_get_all_products_empty(self, db_session):
        """Test getting all products when database is empty."""
        repo = ProductRepository(db_session)
        
        products = repo.get_all()
        
        assert products == []
    
    def test_should_get_all_products_with_data(self, db_session):
        """Test getting all products when database has data."""
        repo = ProductRepository(db_session)
        
        # Create multiple products
        product1_data = ProductCreate(name="Product 1", price=Decimal("10.0"), stock=1)
        product2_data = ProductCreate(name="Product 2", price=Decimal("20.0"), stock=2)
        product3_data = ProductCreate(name="Product 3", price=Decimal("30.0"), stock=3)
        
        created1 = repo.create(product1_data)
        created2 = repo.create(product2_data)
        created3 = repo.create(product3_data)
        
        products = repo.get_all()
        
        assert len(products) == 3
        product_ids = [p.id for p in products]
        assert created1.id in product_ids
        assert created2.id in product_ids
        assert created3.id in product_ids
    
    def test_should_update_existing_product(self, db_session):
        """Test updating an existing product."""
        repo = ProductRepository(db_session)
        
        # Create initial product
        product_data = ProductCreate(
            name="Original Name",
            description="Original description",
            price=Decimal("100.0"),
            stock=10
        )
        created_product = repo.create(product_data)
        
        # Update product
        update_data = ProductUpdate(
            name="Updated Name",
            description="Updated description",
            price=Decimal("150.0"),
            stock=15
        )
        updated_product = repo.update(created_product.id, update_data)
        
        assert updated_product is not None
        assert updated_product.id == created_product.id
        assert updated_product.name == "Updated Name"
        assert updated_product.description == "Updated description"
        assert updated_product.price == Decimal("150.0")
        assert updated_product.stock == 15
    
    def test_should_update_product_partially(self, db_session):
        """Test updating product with only some fields."""
        repo = ProductRepository(db_session)
        
        # Create initial product
        product_data = ProductCreate(
            name="Original Name",
            description="Original description",
            price=Decimal("100.0"),
            stock=10
        )
        created_product = repo.create(product_data)
        
        # Update only name and price
        update_data = ProductUpdate(
            name="New Name",
            price=Decimal("200.0")
        )
        updated_product = repo.update(created_product.id, update_data)
        
        assert updated_product is not None
        assert updated_product.name == "New Name"
        assert updated_product.description == "Original description"  # Unchanged
        assert updated_product.price == Decimal("200.0")
        assert updated_product.stock == 10  # Unchanged
    
    def test_should_return_none_when_updating_nonexistent_product(self, db_session):
        """Test updating non-existent product returns None."""
        repo = ProductRepository(db_session)
        update_data = ProductUpdate(name="New Name")
        
        updated_product = repo.update(999, update_data)
        
        assert updated_product is None
    
    def test_should_delete_existing_product(self, db_session):
        """Test deleting an existing product."""
        repo = ProductRepository(db_session)
        
        # Create product
        product_data = ProductCreate(
            name="To Delete",
            price=Decimal("50.0"),
            stock=5
        )
        created_product = repo.create(product_data)
        
        # Verify it exists
        assert repo.get_by_id(created_product.id) is not None
        
        # Delete it
        result = repo.delete(created_product.id)
        
        assert result is True
        assert repo.get_by_id(created_product.id) is None
    
    def test_should_return_false_when_deleting_nonexistent_product(self, db_session):
        """Test deleting non-existent product returns False."""
        repo = ProductRepository(db_session)
        
        result = repo.delete(999)
        
        assert result is False
    
    def test_should_check_if_product_exists(self, db_session):
        """Test checking if product exists."""
        repo = ProductRepository(db_session)
        
        # Create product
        product_data = ProductCreate(
            name="Exists",
            price=Decimal("25.0"),
            stock=2
        )
        created_product = repo.create(product_data)
        
        # Check existence
        assert repo.exists(created_product.id) is True
        assert repo.exists(999) is False
    
    def test_should_reset_database(self, db_session):
        """Test resetting database removes all products."""
        repo = ProductRepository(db_session)
        
        # Create multiple products
        product1_data = ProductCreate(name="Product 1", price=Decimal("10.0"), stock=1)
        product2_data = ProductCreate(name="Product 2", price=Decimal("20.0"), stock=2)
        
        repo.create(product1_data)
        repo.create(product2_data)
        
        # Verify products exist
        assert len(repo.get_all()) == 2
        
        # Reset database
        repo.reset_database()
        
        # Verify database is empty
        assert len(repo.get_all()) == 0
    
    def test_should_handle_zero_stock_product(self, db_session):
        """Test creating and managing product with zero stock."""
        repo = ProductRepository(db_session)
        product_data = ProductCreate(
            name="Out of Stock",
            price=Decimal("99.99"),
            stock=0
        )
        
        created_product = repo.create(product_data)
        
        assert created_product.stock == 0
        
        # Update to add stock
        update_data = ProductUpdate(stock=5)
        updated_product = repo.update(created_product.id, update_data)
        
        assert updated_product.stock == 5
    
    def test_should_handle_large_price_values(self, db_session):
        """Test handling large price values."""
        repo = ProductRepository(db_session)
        product_data = ProductCreate(
            name="Expensive Item",
            price=Decimal("9999999.99"),
            stock=1
        )
        
        created_product = repo.create(product_data)
        
        assert created_product.price == Decimal("9999999.99")
    
    def test_should_handle_high_stock_values(self, db_session):
        """Test handling high stock values."""
        repo = ProductRepository(db_session)
        product_data = ProductCreate(
            name="Bulk Item",
            price=Decimal("1.0"),
            stock=1000000
        )
        
        created_product = repo.create(product_data)
        
        assert created_product.stock == 1000000