import requests
url = "https://vrl7bye4fnfc3bfos766drpa3y0gjpko.lambda-url.us-west-2.on.aws/"

params = {"name": "Alice"}
response = requests.get(url, params=params)

print(response.status_code)
print(response.text)