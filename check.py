import requests
import json

api_key = "AIzaSyBvkWEZmriAs-20hWZ6z3iRj9cLUag0MdM"

# Test with direct HTTP request
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

headers = {
    'Content-Type': 'application/json',
}

data = {
    "contents": [
        {
            "parts": [
                {"text": "Hello, can you respond?"}
            ]
        }
    ]
}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")