from fastapi.testclient import TestClient
from main import app  # Importing your FastAPI app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to our store full of wonderful products!"}

def test_get_product_by_id():
    product_id = 42
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json() == {"product_id": product_id}

def test_create_product():
    product_data = {
        "name": "Test Product",
        "price": 29.99,
        "description": "A test description",
        "in_stock": True
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 200
    assert response.json() == product_data

def test_create_product_missing_field():
    # Missing required 'name'
    product_data = {
        "price": 29.99,
        "in_stock": True
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 422  # Unprocessable Entity
