# get_request.py
import requests
url = "https://ssykfrrsett4drfk25tryufy7e0wirvp.lambda-url.us-west-2.on.aws/"

params = {"name": "Alice"}
response = requests.get(url, params=params)

print(response.status_code)
print(response.text)