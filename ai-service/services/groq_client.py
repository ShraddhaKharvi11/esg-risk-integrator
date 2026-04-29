import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

print("API KEY:", os.getenv("GROQ_API_KEY"))

client = Groq(api_key=os.getenv("GROQ_API_KEY"))



import time

def call_groq(prompt, retries=2):

    for attempt in range(retries + 1):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Attempt {attempt+1} failed:", str(e))
            time.sleep(1)

    return None

        