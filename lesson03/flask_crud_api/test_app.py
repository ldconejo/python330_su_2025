# test_app.py

import pytest
from app import app, db, User

@pytest.fixture
def client():
    """Creates a test client and initializes a fresh database."""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # In-memory DB for tests

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables for the test database
        yield client  # Provide the test client
        with app.app_context():
            db.drop_all()  # Clean up after tests

def test_create_user(client):
    """Test creating a new user (POST /users/1)."""
    response = client.post("/users/1", json={"name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 201
    assert response.json["name"] == "John Doe"
    assert response.json["email"] == "john@example.com"

def test_get_user(client):
    """Test retrieving an existing user (GET /users/1)."""
    client.post("/users/1", json={"name": "John Doe", "email": "john@example.com"})  # Create user first
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json["name"] == "John Doe"

def test_update_user(client):
    """Test updating a user (PUT /users/1)."""
    client.post("/users/1", json={"name": "John Doe", "email": "john@example.com"})  # Create user first
    response = client.put("/users/1", json={"name": "Jane Doe"})
    assert response.status_code == 200
    assert response.json["name"] == "Jane Doe"

def test_delete_user(client):
    """Test deleting a user (DELETE /users/1)."""
    client.post("/users/1", json={"name": "John Doe", "email": "john@example.com"})  # Create user first
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json["message"] == "User deleted"
    # Verify user no longer exists
    response = client.get("/users/1")
    assert response.status_code == 404

def test_create_user_duplicate_email(client):
    """Test that duplicate emails are not allowed."""
    client.post("/users/1", json={"name": "John Doe", "email": "john@example.com"})  # First user
    response = client.post("/users/2", json={"name": "Jane Doe", "email": "john@example.com"})  # Duplicate email
    assert response.status_code == 400
    assert response.json["message"] == "Email already exists"

def test_create_user_missing_fields(client):
    """Test that creating a user without required fields returns an error."""
    response = client.post("/users/1", json={})
    assert response.status_code == 400
    assert response.json["message"] == "Name and email required"

def test_get_nonexistent_user(client):
    """Test getting a user that does not exist returns 404."""
    response = client.get("/users/999")  # Nonexistent user
    assert response.status_code == 404
    assert response.json["message"] == "User not found"