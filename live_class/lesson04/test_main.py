from fastapi.testclient import TestClient
from main import app

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
            
def test_get_product_by_id_invalid_product_id():
    product_id = "Hello World"
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] in "Input should be a valid integer, unable to parse string as an integer"

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

def test_create_product_invalid_price():
    product_data = {
        "name": "Test Product",
        "price": "No price",
        "description": "A test description",
        "in_stock": True
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid number, unable to parse string as a number"

def test_create_product_get_method():
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == {"message": "Use the POST method for adding a new product"}