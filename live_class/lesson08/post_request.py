import requests

url = "https://vrl7bye4fnfc3bfos766drpa3y0gjpko.lambda-url.us-west-2.on.aws/"

payload = {"name": "Alice", "age": 30}

response = requests.post(url, json=payload)

if response.status_code == 200:
    print(response.status_code)
    print(response.json())
else:
    print("There was an error")
    print(f"Error code: {response.status_code}")
    print(f"Details: {response.text}")