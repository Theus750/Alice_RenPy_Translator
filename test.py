import requests

API_URL = "http://localhost:5000/translate"

text = "Hello, how are you?"
payload = {
    "q": text,
    "source": "en",
    "target": "pt"
}

r = requests.post(API_URL, data=payload)
print("Status code:", r.status_code)
print("Resposta:", r.json())
