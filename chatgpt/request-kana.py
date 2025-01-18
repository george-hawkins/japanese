import requests

def read_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().strip()

API_KEY = read_file("api-key.txt")
ENDPOINT = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

prompt = read_file("prompt.txt")

data = {
    "model": "gpt-4o-mini",
    "messages": [
        {
            "role": "user",
            "content": prompt,
        }
    ],
    "max_tokens": 1000,
    "temperature": 0,
}

response = requests.post(ENDPOINT, headers=headers, json=data)

if response.status_code == 200:
    result = response.json()
    html_output = result["choices"][0]["message"]["content"]
    print(html_output)
else:
    print(f"Error: {response.status_code}, {response.text}")
