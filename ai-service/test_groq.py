from services.groq_client import call_groq

response = call_groq("Say hello in JSON format")

print("Response:", response)