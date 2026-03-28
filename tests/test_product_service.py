import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock

from src.models.product import Product, ProductCreate, ProductUpdate, ProductResponse
from src.services.product_service import ProductService, ProductNotFoundError


class TestProductService:
    """Test ProductService business logic."""
    
    def test_should_create_product_successfully(self):
        """Test creating a product successfully."""
        # Arrange
        mock_repo = Mock()
        mock_product = Product(
            id=1,
            name="Test Product",
            description="A test product",
            price=Decimal("99.99"),
            stock=10
        )
        mock_repo.create.return_value = mock_product
        
        service = ProductService(mock_repo)
        product_data = ProductCreate(
            name="Test Product",
            description="A test product",
            price=Decimal("99.99"),
            stock=10
        )
        
        # Act
        result = service.create_product(product_data)
        
        # Assert
        assert isinstance(result, ProductResponse)
        assert result.id == 1
        assert result.name == "Test Product"
        assert result.description == "A test product"
        assert result.price == Decimal("99.99")
        assert result.stock == 10
        mock_repo.create.assert_called_once_with(product_data)
    
    def test_should_get_product_by_id_successfully(self):
        """Test getting product by ID successfully."""
        # Arrange
        mock_repo = Mock()
        mock_product = Product(
            id=1,
            name="Found Product",
            description="A found product",
            price=Decimal("50.0"),
            stock=5
        )
        mock_repo.get_by_id.return_value = mock_product
        
        service = ProductService(mock_repo)
        
        # Act
        result = service.get_product(1)
        
        # Assert
        assert isinstance(result, ProductResponse)
        assert result.id == 1
        assert result.name == "Found Product"
        assert result.description == "A found product"
        assert result.price == Decimal("50.0")
        assert result.stock == 5
        mock_repo.get_by_id.assert_called_once_with(1)
    
    def test_should_raise_error_when_product_not_found(self):
        """Test getting non-existent product raises error."""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = None
        
        service = ProductService(mock_repo)
        
        # Act & Assert
        with pytest.raises(ProductNotFoundError) as exc_info:
            service.get_product(999)
        
        assert str(exc_info.value) == "Product with id 999 not found"
        mock_repo.get_by_id.assert_called_once_with(999)
    
    def test_should_get_all_products_empty_list(self):
        """Test getting all products when none exist."""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_all.return_value = []
        
        service = ProductService(mock_repo)
        
        # Act
        result = service.get_all_products()
        
        # Assert
        assert result == []
        mock_repo.get_all.assert_called_once()
    
    def test_should_get_all_products_with_data(self):
        """Test getting all products when data exists."""
        # Arrange
        mock_repo = Mock()
        mock_products = [
            Product(id=1, name="Product 1", price=Decimal("10.0"), stock=1),
            Product(id=2, name="Product 2", price=Decimal("20.0"), stock=2),
            Product(id=3, name="Product 3", price=Decimal("30.0"), stock=3)
        ]
        mock_repo.get_all.return_value = mock_products
        
        service = ProductService(mock_repo)
        
        # Act
        result = service.get_all_products()
        
        # Assert
        assert len(result) == 3
        assert all(isinstance(product, ProductResponse) for product in result)
        assert result[0].id == 1
        assert result[0].name == "Product 1"
        assert result[1].id == 2
        assert result[1].name == "Product 2"
        assert result[2].id == 3
        assert result[2].name == "Product 3"
        mock_repo.get_all.assert_called_once()
    
    def test_should_update_product_successfully(self):
        """Test updating product successfully."""
        # Arrange
        mock_repo = Mock()
        mock_updated_product = Product(
            id=1,
            name="Updated Product",
            description="Updated description",
            price=Decimal("150.0"),
            stock=15
        )
        mock_repo.update.return_value = mock_updated_product
        
        service = ProductService(mock_repo)
        update_data = ProductUpdate(
            name="Updated Product",
            description="Updated description",
            price=Decimal("150.0"),
            stock=15
        )
        
        # Act
        result = service.update_product(1, update_data)
        
        # Assert
        assert isinstance(result, ProductResponse)
        assert result.id == 1
        assert result.name == "Updated Product"
        assert result.description == "Updated description"
        assert result.price == Decimal("150.0")
        assert result.stock == 15
        mock_repo.update.assert_called_once_with(1, update_data)
    
    def test_should_raise_error_when_updating_nonexistent_product(self):
        """Test updating non-existent product raises error."""
        # Arrange
        mock_repo = Mock()
        mock_repo.update.return_value = None
        
        service = ProductService(mock_repo)
        update_data = ProductUpdate(name="New Name")
        
        # Act & Assert
        with pytest.raises(ProductNotFoundError) as exc_info:
            service.update_product(999, update_data)
        
        assert str(exc_info.value) == "Product with id 999 not found"
        mock_repo.update.assert_called_once_with(999, update_data)
    
    def test_should_delete_product_successfully(self):
        """Test deleting product successfully."""
        # Arrange
        mock_repo = Mock()
        mock_repo.delete.return_value = True
        
        service = ProductService(mock_repo)
        
        # Act
        result = service.delete_product(1)
        
        # Assert
        assert result is True
        mock_repo.delete.assert_called_once_with(1)
    
    def test_should_raise_error_when_deleting_nonexistent_product(self):
        """Test deleting non-existent product raises error."""
        # Arrange
        mock_repo = Mock()
        mock_repo.delete.return_value = False
        
        service = ProductService(mock_repo)
        
        # Act & Assert
        with pytest.raises(ProductNotFoundError) as exc_info:
            service.delete_product(999)
        
        assert str(exc_info.value) == "Product with id 999 not found"
        mock_repo.delete.assert_called_once_with(999)
    
    def test_should_handle_product_with_none_description(self):
        """Test handling product with None description."""
        # Arrange
        mock_repo = Mock()
        mock_product = Product(
            id=1,
            name="No Description Product",
            description=None,
            price=Decimal("25.0"),
            stock=3
        )
        mock_repo.create.return_value = mock_product
        
        service = ProductService(mock_repo)
        product_data = ProductCreate(
            name="No Description Product",
            price=Decimal("25.0"),
            stock=3
        )
        
        # Act
        result = service.create_product(product_data)
        
        # Assert
        assert result.description is None
        assert result.name == "No Description Product"
    
    def test_should_handle_zero_stock_product(self):
        """Test handling product with zero stock."""
        # Arrange
        mock_repo = Mock()
        mock_product = Product(
            id=1,
            name="Out of Stock",
            price=Decimal("99.99"),
            stock=0
        )
        mock_repo.create.return_value = mock_product
        
        service = ProductService(mock_repo)
        product_data = ProductCreate(
            name="Out of Stock",
            price=Decimal("99.99"),
            stock=0
        )
        
        # Act
        result = service.create_product(product_data)
        
        # Assert
        assert result.stock == 0
        assert result.name == "Out of Stock"
    
    def test_should_handle_partial_update(self):
        """Test handling partial product update."""
        # Arrange
        mock_repo = Mock()
        mock_updated_product = Product(
            id=1,
            name="Updated Name Only",
            description="Original description",
            price=Decimal("100.0"),
            stock=10
        )
        mock_repo.update.return_value = mock_updated_product
        
        service = ProductService(mock_repo)
        update_data = ProductUpdate(name="Updated Name Only")
        
        # Act
        result = service.update_product(1, update_data)
        
        # Assert
        assert result.name == "Updated Name Only"
        assert result.description == "Original description"
        assert result.price == Decimal("100.0")
        assert result.stock == 10
    
    def test_should_convert_product_to_response(self):
        """Test internal conversion from Product to ProductResponse."""
        # Arrange
        mock_repo = Mock()
        service = ProductService(mock_repo)
        
        product = Product(
            id=42,
            name="Conversion Test",
            description="Test conversion",
            price=Decimal("123.45"),
            stock=7
        )
        
        # Act
        result = service._product_to_response(product)
        
        # Assert
        assert isinstance(result, ProductResponse)
        assert result.id == 42
        assert result.name == "Conversion Test"
        assert result.description == "Test conversion"
        assert result.price == Decimal("123.45")
        assert result.stock == 7
    
    def test_should_handle_large_price_values(self):
        """Test handling large price values."""
        # Arrange
        mock_repo = Mock()
        large_price = Decimal("9999999.99")
        mock_product = Product(
            id=1,
            name="Expensive Item",
            price=large_price,
            stock=1
        )
        mock_repo.create.return_value = mock_product
        
        service = ProductService(mock_repo)
        product_data = ProductCreate(
            name="Expensive Item",
            price=large_price,
            stock=1
        )
        
        # Act
        result = service.create_product(product_data)
        
        # Assert
        assert result.price == large_price
    
    def test_should_handle_high_stock_values(self):
        """Test handling high stock values."""
        # Arrange
        mock_repo = Mock()
        high_stock = 1000000
        mock_product = Product(
            id=1,
            name="Bulk Item",
            price=Decimal("1.0"),
            stock=high_stock
        )
        mock_repo.create.return_value = mock_product
        
        service = ProductService(mock_repo)
        product_data = ProductCreate(
            name="Bulk Item",
            price=Decimal("1.0"),
            stock=high_stock
        )
        
        # Act
        result = service.create_product(product_data)
        
        # Assert
        assert result.stock == high_stock