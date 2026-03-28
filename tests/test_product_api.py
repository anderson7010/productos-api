import pytest
from decimal import Decimal


class TestProductAPI:
    """Test Product API endpoints integration."""
    
    def test_should_create_product_successfully(self, client):
        """Test POST /products/ creates product successfully."""
        product_data = {
            "name": "Test Product",
            "description": "A test product",
            "price": 99.99,
            "stock": 10
        }
        
        response = client.post("/products/", json=product_data)
        
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["id"] is not None
        assert data["name"] == "Test Product"
        assert data["description"] == "A test product"
        assert str(data["price"]) == "99.99"
        assert data["stock"] == 10
    
    def test_should_create_product_without_description(self, client):
        """Test creating product without description."""
        product_data = {
            "name": "No Description Product",
            "price": 50.0,
            "stock": 5
        }
        
        response = client.post("/products/", json=product_data)
        
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["name"] == "No Description Product"
        assert data["description"] is None
        assert str(data["price"]) == "50.0"
        assert data["stock"] == 5
    
    def test_should_reject_invalid_product_data(self, client):
        """Test POST /products/ rejects invalid data."""
        invalid_data = {
            "name": "",  # Empty name
            "price": -10.0,  # Negative price
            "stock": -1  # Negative stock
        }
        
        response = client.post("/products/", json=invalid_data)
        
        assert response.status_code == 422, response.text
    
    def test_should_reject_missing_required_fields(self, client):
        """Test POST /products/ rejects missing required fields."""
        incomplete_data = {
            "name": "Incomplete Product"
            # Missing price and stock
        }
        
        response = client.post("/products/", json=incomplete_data)
        
        assert response.status_code == 422, response.text
    
    def test_should_get_all_products_empty(self, client):
        """Test GET /products/ returns empty list when no products exist."""
        response = client.get("/products/")
        
        assert response.status_code == 200, response.text
        data = response.json()
        assert data == []
    
    def test_should_get_all_products_with_data(self, client):
        """Test GET /products/ returns all products."""
        # Create multiple products
        products_data = [
            {"name": "Product 1", "price": 10.0, "stock": 1},
            {"name": "Product 2", "price": 20.0, "stock": 2},
            {"name": "Product 3", "price": 30.0, "stock": 3}
        ]
        
        created_ids = []
        for product_data in products_data:
            response = client.post("/products/", json=product_data)
            assert response.status_code == 201, response.text
            created_ids.append(response.json()["id"])
        
        # Get all products
        response = client.get("/products/")
        
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 3
        
        # Verify all created products are returned
        returned_ids = [product["id"] for product in data]
        for created_id in created_ids:
            assert created_id in returned_ids
    
    def test_should_get_product_by_id_successfully(self, client):
        """Test GET /products/{id} returns specific product."""
        # Create a product
        product_data = {
            "name": "Findable Product",
            "description": "A findable product",
            "price": 75.0,
            "stock": 8
        }
        create_response = client.post("/products/", json=product_data)
        assert create_response.status_code == 201, create_response.text
        created_product = create_response.json()
        
        # Get the product by ID
        response = client.get(f"/products/{created_product['id']}")
        
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["id"] == created_product["id"]
        assert data["name"] == "Findable Product"
        assert data["description"] == "A findable product"
        assert str(data["price"]) == "75.0"
        assert data["stock"] == 8
    
    def test_should_return_404_for_nonexistent_product(self, client):
        """Test GET /products/{id} returns 404 for non-existent product."""
        response = client.get("/products/999")
        
        assert response.status_code == 404, response.text
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    def test_should_update_product_successfully(self, client):
        """Test PUT /products/{id} updates product successfully."""
        # Create a product
        product_data = {
            "name": "Original Product",
            "description": "Original description",
            "price": 100.0,
            "stock": 10
        }
        create_response = client.post("/products/", json=product_data)
        assert create_response.status_code == 201, create_response.text
        created_product = create_response.json()
        
        # Update the product
        update_data = {
            "name": "Updated Product",
            "description": "Updated description",
            "price": 150.0,
            "stock": 15
        }
        response = client.put(f"/products/{created_product['id']}", json=update_data)
        
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["id"] == created_product["id"]
        assert data["name"] == "Updated Product"
        assert data["description"] == "Updated description"
        assert str(data["price"]) == "150.0"
        assert data["stock"] == 15
    
    def test_should_update_product_partially(self, client):
        """Test PUT /products/{id} with partial update."""
        # Create a product
        product_data = {
            "name": "Original Product",
            "description": "Original description",
            "price": 100.0,
            "stock": 10
        }
        create_response = client.post("/products/", json=product_data)
        assert create_response.status_code == 201, create_response.text
        created_product = create_response.json()
        
        # Update only name and price
        update_data = {
            "name": "Partially Updated",
            "price": 200.0
        }
        response = client.put(f"/products/{created_product['id']}", json=update_data)
        
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "Partially Updated"
        assert data["description"] == "Original description"  # Unchanged
        assert str(data["price"]) == "200.0"
        assert data["stock"] == 10  # Unchanged
    
    def test_should_return_404_when_updating_nonexistent_product(self, client):
        """Test PUT /products/{id} returns 404 for non-existent product."""
        update_data = {
            "name": "Updated Name",
            "price": 50.0,
            "stock": 5
        }
        
        response = client.put("/products/999", json=update_data)
        
        assert response.status_code == 404, response.text
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    def test_should_reject_invalid_update_data(self, client):
        """Test PUT /products/{id} rejects invalid update data."""
        # Create a product first
        product_data = {
            "name": "Valid Product",
            "price": 50.0,
            "stock": 5
        }
        create_response = client.post("/products/", json=product_data)
        assert create_response.status_code == 201, create_response.text
        created_product = create_response.json()
        
        # Try to update with invalid data
        invalid_update = {
            "name": "",  # Empty name
            "price": -10.0,  # Negative price
            "stock": -1  # Negative stock
        }
        
        response = client.put(f"/products/{created_product['id']}", json=invalid_update)
        
        assert response.status_code == 422, response.text
    
    def test_should_delete_product_successfully(self, client):
        """Test DELETE /products/{id} deletes product successfully."""
        # Create a product
        product_data = {
            "name": "To Delete",
            "price": 25.0,
            "stock": 3
        }
        create_response = client.post("/products/", json=product_data)
        assert create_response.status_code == 201, create_response.text
        created_product = create_response.json()
        
        # Delete the product
        response = client.delete(f"/products/{created_product['id']}")
        
        assert response.status_code == 204, response.text
        
        # Verify product is deleted
        get_response = client.get(f"/products/{created_product['id']}")
        assert get_response.status_code == 404, get_response.text
    
    def test_should_return_404_when_deleting_nonexistent_product(self, client):
        """Test DELETE /products/{id} returns 404 for non-existent product."""
        response = client.delete("/products/999")
        
        assert response.status_code == 404, response.text
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    def test_should_handle_zero_stock_product(self, client):
        """Test handling product with zero stock."""
        product_data = {
            "name": "Out of Stock",
            "price": 99.99,
            "stock": 0
        }
        
        response = client.post("/products/", json=product_data)
        
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["stock"] == 0
    
    def test_should_handle_large_price_values(self, client):
        """Test handling large price values."""
        product_data = {
            "name": "Expensive Item",
            "price": 9999999.99,
            "stock": 1
        }
        
        response = client.post("/products/", json=product_data)
        
        assert response.status_code == 201, response.text
        data = response.json()
        assert str(data["price"]) == "9999999.99"
    
    def test_should_handle_high_stock_values(self, client):
        """Test handling high stock values."""
        product_data = {
            "name": "Bulk Item",
            "price": 1.0,
            "stock": 1000000
        }
        
        response = client.post("/products/", json=product_data)
        
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["stock"] == 1000000
    
    def test_should_maintain_data_consistency_across_operations(self, client):
        """Test data consistency across multiple operations."""
        # Create product
        product_data = {
            "name": "Consistency Test",
            "description": "Testing consistency",
            "price": 100.0,
            "stock": 10
        }
        create_response = client.post("/products/", json=product_data)
        assert create_response.status_code == 201, create_response.text
        created_product = create_response.json()
        product_id = created_product["id"]
        
        # Get product and verify data
        get_response = client.get(f"/products/{product_id}")
        assert get_response.status_code == 200, get_response.text
        get_data = get_response.json()
        assert get_data == created_product
        
        # Update product
        update_data = {
            "name": "Updated Consistency Test",
            "price": 150.0
        }
        update_response = client.put(f"/products/{product_id}", json=update_data)
        assert update_response.status_code == 200, update_response.text
        updated_product = update_response.json()
        
        # Verify update in get all
        all_response = client.get("/products/")
        assert all_response.status_code == 200, all_response.text
        all_products = all_response.json()
        found_product = next((p for p in all_products if p["id"] == product_id), None)
        assert found_product is not None
        assert found_product["name"] == "Updated Consistency Test"
        assert str(found_product["price"]) == "150.0"
        
        # Delete product
        delete_response = client.delete(f"/products/{product_id}")
        assert delete_response.status_code == 204, delete_response.text
        
        # Verify deletion in get all
        final_all_response = client.get("/products/")
        assert final_all_response.status_code == 200, final_all_response.text
        final_all_products = final_all_response.json()
        assert not any(p["id"] == product_id for p in final_all_products)