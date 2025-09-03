# double_test.py
import requests
import json

# Replace this with your actual Lambda Function URL
LAMBDA_URL = "https://ssykfrrsett4drfk25tryufy7e0wirvp.lambda-url.us-west-2.on.aws/"

def test_get_request():
    params = {"name": "Alice"}
    response = requests.get(LAMBDA_URL, params=params)

    print("\n--- GET Request ---")
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

def test_post_request():
    data = {"name": "Bob"}
    headers = {"Content-Type": "application/json"}
    response = requests.post(LAMBDA_URL, headers=headers, json=data)

    print("\n--- POST Request ---")
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

if __name__ == "__main__":
    test_get_request()
    test_post_request()