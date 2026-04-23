import os
import requests
from dotenv import load_dotenv
import time

# Load API key
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def generate_response(prompt, retries=3):
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    for attempt in range(retries):
        try:
            response = requests.post(URL, headers=HEADERS, json=data, timeout=10)
            result = response.json()

            if "choices" in result:
                return result["choices"][0]["message"]["content"]
            else:
                print("⚠️ API Error:", result)

        except Exception as e:
            print(f"❌ Attempt {attempt+1} failed:", e)
            time.sleep(2)

    return "⚠️ Failed to get response from AI"