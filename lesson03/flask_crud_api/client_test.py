import requests

BASE_URL = "http://127.0.0.1:5000"

def test_home():
    print("GET /")
    response = requests.get(f"{BASE_URL}/")
    print(response.status_code, response.json())

def create_user(user_id, name, email):
    print(f"POST /users/{user_id}")
    data = {"name": name, "email": email}
    response = requests.post(f"{BASE_URL}/users/{user_id}", json=data)
    print(response.status_code, response.json())

def get_user(user_id):
    print(f"GET /users/{user_id}")
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    print(response.status_code, response.json())

def update_user(user_id, name=None, email=None):
    print(f"PUT /users/{user_id}")
    data = {}
    if name: data["name"] = name
    if email: data["email"] = email
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=data)
    print(response.status_code, response.json())

def delete_user(user_id):
    print(f"DELETE /users/{user_id}")
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    print(response.status_code, response.json())

if __name__ == "__main__":
    test_home()

    user_id = 1
    create_user(user_id, "Alice", "alice@example.com")
    get_user(user_id)

    update_user(user_id, name="Alice Smith")
    get_user(user_id)

    delete_user(user_id)
    get_user(user_id)  # Should now return 404
