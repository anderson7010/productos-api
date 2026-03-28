import pytest
from decimal import Decimal
from pydantic import ValidationError

from src.models.product import ProductCreate, ProductUpdate, ProductResponse


class TestProductCreate:
    """Test ProductCreate schema validation."""
    
    def test_should_create_valid_product(self):
        """Test creating a valid product."""
        product_data = {
            "name": "Test Product",
            "description": "A test product",
            "price": 99.99,
            "stock": 10
        }
        product = ProductCreate(**product_data)
        
        assert product.name == "Test Product"
        assert product.description == "A test product"
        assert product.price == Decimal("99.99")
        assert product.stock == 10
    
    def test_should_create_product_with_minimal_fields(self):
        """Test creating product with only required fields."""
        product_data = {
            "name": "Minimal Product",
            "price": 50.0,
            "stock": 5
        }
        product = ProductCreate(**product_data)
        
        assert product.name == "Minimal Product"
        assert product.description is None
        assert product.price == Decimal("50.0")
        assert product.stock == 5
    
    def test_should_reject_empty_name(self):
        """Test validation fails for empty name."""
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(name="", price=10.0, stock=1)
        
        errors = exc_info.value.errors()
        assert any(error["type"] == "string_too_short" for error in errors)
    
    def test_should_reject_negative_price(self):
        """Test validation fails for negative price."""
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(name="Test", price=-10.0, stock=1)
        
        errors = exc_info.value.errors()
        assert any(error["type"] == "greater_than" for error in errors)
    
    def test_should_reject_zero_price(self):
        """Test validation fails for zero price."""
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(name="Test", price=0.0, stock=1)
        
        errors = exc_info.value.errors()
        assert any(error["type"] == "greater_than" for error in errors)
    
    def test_should_reject_negative_stock(self):
        """Test validation fails for negative stock."""
        with pytest.raises(ValidationError) as exc_info:
            ProductCreate(name="Test", price=10.0, stock=-1)
        
        errors = exc_info.value.errors()
        assert any(error["type"] == "greater_than_equal" for error in errors)
    
    def test_should_accept_zero_stock(self):
        """Test validation accepts zero stock."""
        product = ProductCreate(name="Out of Stock", price=10.0, stock=0)
        assert product.stock == 0
    
    def test_should_handle_long_description(self):
        """Test handling of long description."""
        long_description = "A" * 1000
        product = ProductCreate(
            name="Test",
            description=long_description,
            price=10.0,
            stock=1
        )
        assert product.description == long_description


class TestProductUpdate:
    """Test ProductUpdate schema validation."""
    
    def test_should_create_update_with_all_fields(self):
        """Test creating update with all fields."""
        update_data = {
            "name": "Updated Product",
            "description": "Updated description",
            "price": 199.99,
            "stock": 20
        }
        product_update = ProductUpdate(**update_data)
        
        assert product_update.name == "Updated Product"
        assert product_update.description == "Updated description"
        assert product_update.price == Decimal("199.99")
        assert product_update.stock == 20
    
    def test_should_create_update_with_partial_fields(self):
        """Test creating update with only some fields."""
        product_update = ProductUpdate(name="New Name")
        
        assert product_update.name == "New Name"
        assert product_update.description is None
        assert product_update.price is None
        assert product_update.stock is None
    
    def test_should_create_empty_update(self):
        """Test creating update with no fields."""
        product_update = ProductUpdate()
        
        assert product_update.name is None
        assert product_update.description is None
        assert product_update.price is None
        assert product_update.stock is None
    
    def test_should_reject_empty_name_when_provided(self):
        """Test validation fails for empty name when provided."""
        with pytest.raises(ValidationError) as exc_info:
            ProductUpdate(name="")
        
        errors = exc_info.value.errors()
        assert any(error["type"] == "string_too_short" for error in errors)
    
    def test_should_reject_negative_price_when_provided(self):
        """Test validation fails for negative price when provided."""
        with pytest.raises(ValidationError) as exc_info:
            ProductUpdate(price=-5.0)
        
        errors = exc_info.value.errors()
        assert any(error["type"] == "greater_than" for error in errors)
    
    def test_should_reject_negative_stock_when_provided(self):
        """Test validation fails for negative stock when provided."""
        with pytest.raises(ValidationError) as exc_info:
            ProductUpdate(stock=-1)
        
        errors = exc_info.value.errors()
        assert any(error["type"] == "greater_than_equal" for error in errors)


class TestProductResponse:
    """Test ProductResponse schema."""
    
    def test_should_create_response_with_all_fields(self):
        """Test creating response with all fields."""
        response_data = {
            "id": 1,
            "name": "Response Product",
            "description": "Response description",
            "price": 299.99,
            "stock": 15
        }
        product_response = ProductResponse(**response_data)
        
        assert product_response.id == 1
        assert product_response.name == "Response Product"
        assert product_response.description == "Response description"
        assert product_response.price == Decimal("299.99")
        assert product_response.stock == 15
    
    def test_should_create_response_with_none_description(self):
        """Test creating response with None description."""
        response_data = {
            "id": 2,
            "name": "No Description Product",
            "description": None,
            "price": 99.99,
            "stock": 5
        }
        product_response = ProductResponse(**response_data)
        
        assert product_response.id == 2
        assert product_response.name == "No Description Product"
        assert product_response.description is None
        assert product_response.price == Decimal("99.99")
        assert product_response.stock == 5
    
    def test_should_require_id_field(self):
        """Test that id field is required."""
        with pytest.raises(ValidationError) as exc_info:
            ProductResponse(
                name="Test",
                price=10.0,
                stock=1
            )
        
        errors = exc_info.value.errors()
        assert any(error["type"] == "missing" and "id" in str(error) for error in errors)
    
    def test_should_require_name_field(self):
        """Test that name field is required."""
        with pytest.raises(ValidationError) as exc_info:
            ProductResponse(
                id=1,
                price=10.0,
                stock=1
            )
        
        errors = exc_info.value.errors()
        assert any(error["type"] == "missing" and "name" in str(error) for error in errors)
    
    def test_should_require_price_field(self):
        """Test that price field is required."""
        with pytest.raises(ValidationError) as exc_info:
            ProductResponse(
                id=1,
                name="Test",
                stock=1
            )
        
        errors = exc_info.value.errors()
        assert any(error["type"] == "missing" and "price" in str(error) for error in errors)
    
    def test_should_require_stock_field(self):
        """Test that stock field is required."""
        with pytest.raises(ValidationError) as exc_info:
            ProductResponse(
                id=1,
                name="Test",
                price=10.0
            )
        
        errors = exc_info.value.errors()
        assert any(error["type"] == "missing" and "stock" in str(error) for error in errors)