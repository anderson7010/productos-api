import pytest
from pydantic import ValidationError
from src.models import ProductCreate


class TestCreateProduct:
    """Tests for POST /products endpoint."""

    def test_should_create_product_with_valid_data(self, client):
        payload = {"name": "Laptop Gamer", "price": 1500.00, "category": "Electronics"}
        response = client.post("/products", json=payload)
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Laptop Gamer"
        assert float(data["price"]) == pytest.approx(1500.00)
        assert data["category"] == "Electronics"

    def test_should_create_product_without_category(self, client):
        payload = {"name": "Mouse Básico", "price": 25.50}
        response = client.post("/products", json=payload)
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Mouse Básico"
        assert float(data["price"]) == pytest.approx(25.50)
        assert data["category"] is None

    def test_should_assign_incremental_ids(self, client):
        payload1 = {"name": "Producto 1", "price": 10.00}
        payload2 = {"name": "Producto 2", "price": 20.00}
        response1 = client.post("/products", json=payload1)
        response2 = client.post("/products", json=payload2)
        assert response1.status_code == 201, response1.text
        assert response2.status_code == 201, response2.text
        assert response1.json()["id"] == 1
        assert response2.json()["id"] == 2

    def test_should_reject_empty_name(self, client):
        payload = {"name": "", "price": 10.00}
        response = client.post("/products", json=payload)
        assert response.status_code == 422, response.text

    def test_should_reject_missing_name(self, client):
        payload = {"price": 10.00}
        response = client.post("/products", json=payload)
        assert response.status_code == 422, response.text

    def test_should_reject_negative_price(self, client):
        payload = {"name": "Producto", "price": -5.00}
        response = client.post("/products", json=payload)
        assert response.status_code == 422, response.text

    def test_should_reject_zero_price(self, client):
        payload = {"name": "Producto", "price": 0}
        response = client.post("/products", json=payload)
        assert response.status_code == 422, response.text

    def test_should_reject_missing_price(self, client):
        payload = {"name": "Producto"}
        response = client.post("/products", json=payload)
        assert response.status_code == 422, response.text

    def test_should_reject_non_numeric_price(self, client):
        payload = {"name": "Producto", "price": "gratis"}
        response = client.post("/products", json=payload)
        assert response.status_code == 422, response.text

    def test_should_reject_empty_body(self, client):
        response = client.post("/products", json={})
        assert response.status_code == 422, response.text


class TestListProducts:
    """Tests for GET /products endpoint."""

    def test_should_return_empty_list_when_no_products(self, client):
        response = client.get("/products")
        assert response.status_code == 200, response.text
        assert response.json() == []

    def test_should_return_all_products(self, client):
        client.post("/products", json={"name": "Producto 1", "price": 10.00})
        client.post("/products", json={"name": "Producto 2", "price": 20.00})
        response = client.get("/products")
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 2

    def test_should_return_products_with_correct_structure(self, client):
        client.post("/products", json={"name": "Teclado", "price": 45.99, "category": "Periféricos"})
        response = client.get("/products")
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 1
        product = data[0]
        assert "id" in product
        assert "name" in product
        assert "price" in product
        assert "category" in product
        assert product["name"] == "Teclado"
        assert float(product["price"]) == pytest.approx(45.99)
        assert product["category"] == "Periféricos"


class TestGetProductById:
    """Tests for GET /products/{product_id} endpoint."""

    def test_should_return_product_by_id(self, client):
        create_response = client.post("/products", json={"name": "Monitor", "price": 300.00, "category": "Electronics"})
        assert create_response.status_code == 201, create_response.text
        product_id = create_response.json()["id"]

        response = client.get(f"/products/{product_id}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["id"] == product_id
        assert data["name"] == "Monitor"
        assert float(data["price"]) == pytest.approx(300.00)
        assert data["category"] == "Electronics"

    def test_should_return_404_for_nonexistent_product(self, client):
        response = client.get("/products/999")
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Producto no encontrado"

    def test_should_return_404_for_id_zero(self, client):
        response = client.get("/products/0")
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Producto no encontrado"

    def test_should_return_422_for_non_integer_id(self, client):
        response = client.get("/products/abc")
        assert response.status_code == 422, response.text


class TestProductCreateModelValidation:
    """Tests for Pydantic model validation of ProductCreate."""

    def test_should_reject_empty_name_at_model_level(self):
        with pytest.raises(ValidationError):
            ProductCreate(name="", price=10.00)

    def test_should_reject_negative_price_at_model_level(self):
        with pytest.raises(ValidationError):
            ProductCreate(name="Test", price=-1.0)

    def test_should_reject_zero_price_at_model_level(self):
        with pytest.raises(ValidationError):
            ProductCreate(name="Test", price=0)

    def test_should_accept_valid_product_at_model_level(self):
        product = ProductCreate(name="Valid Product", price=9.99, category="Test")
        assert product.name == "Valid Product"
        assert float(product.price) == pytest.approx(9.99)
        assert product.category == "Test"

    def test_should_accept_product_without_category_at_model_level(self):
        product = ProductCreate(name="No Category", price=5.00)
        assert product.category is None
