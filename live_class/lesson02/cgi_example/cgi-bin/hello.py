#!/usr/bin/env python
import os
import urllib.parse

print("Content-Type: text/html\n")

query_string = os.environ.get('QUERY_STRING', '')

params = urllib.parse.parse_qs(query_string)

print(params)

name = params.get('name', ['World'])[0]

print(f"<html><body><h1>Hello, {name}!</h1></body></html>")
