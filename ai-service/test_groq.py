import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {"role": "user", "content": "Explain ESG in simple words"}
    ]
}

response = requests.post(url, headers=headers, json=data)
result = response.json()

print("\n🔍 FULL RESPONSE:\n", result)

if "choices" in result:
    print("\n✅ AI Response:\n")
    print(result["choices"][0]["message"]["content"])
else:
    print("\n❌ API Error:\n")
    print(result)