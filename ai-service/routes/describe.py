from flask import Blueprint, request, jsonify
from datetime import datetime
from pathlib import Path
from services.groq_client import call_groq
import json

describe_bp = Blueprint("describe", __name__)

@describe_bp.route("/describe", methods=["POST"])
def describe():

    data = request.get_json()

    # ✅ 1. Validate input
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    user_input = data["text"].strip()

    if not user_input:
        return jsonify({"error": "Empty input"}), 400

    # 🔥 LOG INPUT (HERE)
    print("INPUT:", user_input)

    # ✅ 2. Load prompt
    prompt_template = Path("prompts/describe_prompt.txt").read_text()
    prompt = prompt_template.replace("{input}", user_input)

    # ✅ 3. Call Groq
    ai_response = call_groq(prompt)

    # 🔥 LOG RAW AI RESPONSE (HERE)
    print("RAW AI:", ai_response)

    if not ai_response:
        return jsonify({"error": "AI service unavailable"}), 500

    # ✅ 4. Parse JSON safely
    try:
        result = json.loads(ai_response)
    except:
        return jsonify({"error": "Invalid AI response", "raw": ai_response}), 500

    # ✅ 5. Add timestamp
    result["generated_at"] = datetime.utcnow().isoformat()

    return jsonify(result)