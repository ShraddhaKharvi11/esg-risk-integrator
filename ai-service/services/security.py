import re

# Remove HTML/script tags
def sanitize_input(value):
    if not isinstance(value, str):
        return value
    value = re.sub(r'<.*?>', '', value)  # remove HTML tags
    return value.strip()

# Basic prompt-injection patterns
BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "reveal system prompt",
    "act as system",
    "bypass",
]

def is_malicious(text):
    if not isinstance(text, str):
        return False
    text_lower = text.lower()
    return any(p in text_lower for p in BLOCKED_PATTERNS)