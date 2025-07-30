import pytest
from app import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_create_user(client):
    response = client.post('/users/1', json={'name': 'Alice', 'email': 'alice@example.com'})
    assert response.status_code == 201
    assert response.json == {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'}

def test_get_user(client):
    client.post('/users/1', json={'name': 'Alice', 'email': 'alice@example.com'})
    response = client.get('/users/1')
    assert response.status_code == 200
    assert response.json == {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'}
    assert response.json['name'] == 'Alice'

def test_get_nonexistent_user(client):
    response = client.get('/users/999')
    assert response.status_code == 404
    assert response.json == {'message': 'User not found'}

def test_update_user(client):
    client.post('/users/1', json={'name': 'Alice', 'email': 'alice@example.com'})
    response = client.patch('/users/1', json={'name': 'Alice Smith', 'email': 'asmith@example.com'})
    assert response.status_code == 200
    assert response.json['name'] == 'Alice Smith'
    assert response.json['email'] == 'asmith@example.com'

def test_delete_user(client):
    client.post('/users/1', json={'name': 'Alice', 'email': 'alice@example.com'})
    response = client.delete('/users/1')
    assert response.status_code == 200
    assert response.json == {'message': 'User deleted successfully'}
    response = client.get('/users/1')
    assert response.status_code == 404

def test_delete_nonexistent_user(client):
    response = client.delete('/users/999')
    assert response.status_code == 404
    assert response.json == {'message': 'User not found'}