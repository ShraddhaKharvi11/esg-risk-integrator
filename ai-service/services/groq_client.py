import os
import requests
from dotenv import load_dotenv
import time
import json
import re

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Simple in-memory cache
CACHE = {}


def _fallback():
    return {
        "title": "ESG Report",
        "summary": "Fallback response due to AI error.",
        "overview": "Basic overview unavailable.",
        "risks": ["Data unavailable"],
        "recommendations": ["Retry later"],
        "is_fallback": True
    }


def get_cache_key(prompt):
    return hash(prompt)


def clean_ai_response(content):
    content = re.sub(r"```json", "", content)
    content = re.sub(r"```", "", content)
    return content.strip()


def generate_response(prompt, retries=3):
    cache_key = get_cache_key(prompt)

    # Return cached response if available
    if cache_key in CACHE:
        return CACHE[cache_key]

    data = {
        "model": "llama-3.3-70b-versatile",
        "temperature": 0.2,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    for attempt in range(retries):
        try:
            response = requests.post(
                URL,
                headers=HEADERS,
                json=data,
                timeout=6
            )

            result = response.json()

            if "choices" in result:
                content = result["choices"][0]["message"]["content"]
                content = clean_ai_response(content)

                json_match = re.search(r"\{[\s\S]*\}", content)

                if json_match:
                    json_str = json_match.group()

                    try:
                        parsed = json.loads(json_str)
                        parsed["is_fallback"] = False

                        # Cache successful response
                        CACHE[cache_key] = parsed

                        return parsed

                    except:
                        pass

                fallback_response = {
                    "title": "ESG Report",
                    "summary": "AI response not structured properly.",
                    "overview": content[:500],
                    "risks": ["Could not extract risks"],
                    "recommendations": ["Retry request"],
                    "is_fallback": True
                }

                CACHE[cache_key] = fallback_response

                return fallback_response

        except Exception as e:
            print(f"Attempt {attempt+1} failed:", e)
            time.sleep(2)

    fallback_response = _fallback()

    CACHE[cache_key] = fallback_response

    return fallback_response