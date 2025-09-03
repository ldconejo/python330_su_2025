# post_request.py
import requests
import json

url = "https://ssykfrrsett4drfk25tryufy7e0wirvp.lambda-url.us-west-2.on.aws/"
payload = {"name": "Alice", "age": 30}
response = requests.post(url, json=payload)

print(response.status_code)
print(response.json())