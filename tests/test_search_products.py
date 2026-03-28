import pytest


def _create_product(client, name, price=100.00, category=None):
    """Helper to create a product and return the response data."""
    payload = {"name": name, "price": price}
    if category is not None:
        payload["category"] = category
    response = client.post("/products", json=payload)
    assert response.status_code == 201, response.text
    return response.json()


class TestSearchProductsByName:
    """Tests for GET /products/search?name=<query> endpoint."""

    def test_should_find_product_by_exact_name(self, client):
        _create_product(client, "Laptop Gamer")
        response = client.get("/products/search", params={"name": "Laptop Gamer"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Laptop Gamer"

    def test_should_find_products_by_partial_match(self, client):
        _create_product(client, "Laptop Gamer")
        _create_product(client, "Laptop Oficina")
        _create_product(client, "Teclado Mecánico")
        response = client.get("/products/search", params={"name": "Laptop"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 2
        names = [p["name"] for p in data]
        assert "Laptop Gamer" in names
        assert "Laptop Oficina" in names

    def test_should_search_case_insensitive(self, client):
        _create_product(client, "Laptop Gamer")
        response = client.get("/products/search", params={"name": "laptop gamer"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Laptop Gamer"

    def test_should_search_case_insensitive_uppercase(self, client):
        _create_product(client, "Laptop Gamer")
        response = client.get("/products/search", params={"name": "LAPTOP GAMER"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Laptop Gamer"

    def test_should_search_case_insensitive_mixed_case(self, client):
        _create_product(client, "Laptop Gamer")
        response = client.get("/products/search", params={"name": "lApToP"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 1

    def test_should_return_empty_list_when_no_match(self, client):
        _create_product(client, "Laptop Gamer")
        response = client.get("/products/search", params={"name": "Teclado"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert data == []

    def test_should_return_empty_list_when_store_is_empty(self, client):
        response = client.get("/products/search", params={"name": "Laptop"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert data == []

    def test_should_return_400_for_empty_name_query(self, client):
        response = client.get("/products/search", params={"name": ""})
        assert response.status_code == 400, response.text
        data = response.json()
        assert data["detail"] == "El parámetro 'name' no puede estar vacío"

    def test_should_return_400_for_whitespace_only_query(self, client):
        response = client.get("/products/search", params={"name": "   "})
        assert response.status_code == 400, response.text
        data = response.json()
        assert data["detail"] == "El parámetro 'name' no puede estar vacío"

    def test_should_find_product_with_special_characters(self, client):
        _create_product(client, "Ratón USB 2.0")
        response = client.get("/products/search", params={"name": "USB 2.0"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Ratón USB 2.0"

    def test_should_return_correct_product_structure_in_search(self, client):
        _create_product(client, "Monitor 4K", price=599.99, category="Pantallas")
        response = client.get("/products/search", params={"name": "Monitor"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 1
        product = data[0]
        assert "id" in product
        assert product["name"] == "Monitor 4K"
        assert float(product["price"]) == pytest.approx(599.99)
        assert product["category"] == "Pantallas"

    def test_should_find_single_character_substring(self, client):
        _create_product(client, "A")
        _create_product(client, "B")
        response = client.get("/products/search", params={"name": "A"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "A"

    def test_should_find_all_products_with_common_substring(self, client):
        _create_product(client, "Cable USB")
        _create_product(client, "Hub USB")
        _create_product(client, "Adaptador USB")
        _create_product(client, "Teclado Bluetooth")
        response = client.get("/products/search", params={"name": "USB"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 3

    def test_should_handle_query_with_leading_trailing_spaces(self, client):
        _create_product(client, "Laptop Gamer")
        response = client.get("/products/search", params={"name": "  Laptop  "})
        assert response.status_code == 200, response.text
        data = response.json()
        # After strip(), the query becomes "Laptop" which should match
        assert len(data) == 1
        assert data[0]["name"] == "Laptop Gamer"

    def test_search_endpoint_should_not_conflict_with_get_by_id(self, client):
        """Ensure /products/search is not interpreted as /products/{product_id}."""
        _create_product(client, "Test Product")
        response = client.get("/products/search", params={"name": "Test"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 1

    def test_should_find_product_with_numeric_name(self, client):
        _create_product(client, "12345")
        response = client.get("/products/search", params={"name": "123"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "12345"

    def test_should_return_multiple_results_preserving_all_fields(self, client):
        _create_product(client, "Laptop Dell", price=1200.00, category="Computadoras")
        _create_product(client, "Laptop HP", price=1100.00, category="Computadoras")
        response = client.get("/products/search", params={"name": "Laptop"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 2
        for product in data:
            assert "id" in product
            assert "name" in product
            assert "price" in product
            assert "category" in product
            assert product["category"] == "Computadoras"
