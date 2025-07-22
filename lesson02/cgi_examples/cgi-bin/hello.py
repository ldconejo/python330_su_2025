#!/usr/bin/env python
import os
import urllib.parse

print("Content-Type: text/html\n")  # HTTP header  

# Get the query string from environment variables
query_string = os.environ.get("QUERY_STRING", "")

# Parse query parameters
params = urllib.parse.parse_qs(query_string)
name = params.get("name", ["World"])[0]  # Default to "World" if no name is provided

# Generate response
print(f"<html><body><h1>Hello, {name}!</h1></body></html>")