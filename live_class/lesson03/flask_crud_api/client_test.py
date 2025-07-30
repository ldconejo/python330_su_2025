import requests

BASE_URL = "http://127.0.0.1:5000"

def create_user(user_id, name, email):
    print(f"POST /users/{user_id}")
    data = {"name": name, "email": email}
    response = requests.post(f"{BASE_URL}/users/{user_id}", json=data)
    print(f"Response: {response.status_code} - {response.json()}")

def update_user(user_id, name=None, email=None):
    print(f"PUT /users/{user_id}")
    data = {}
    if name:
        data['name'] = name
    if email:
        data['email'] = email
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=data)
    print(f"Response: {response.status_code} - {response.json()}")

if __name__ == "__main__":
    #create_user(123, "John Doe", "jdoe@example.com")
    update_user(124)