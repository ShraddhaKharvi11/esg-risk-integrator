from flask import Blueprint, request, jsonify
from datetime import datetime
from pathlib import Path
from services.groq_client import call_groq
import json
import re

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

    print("INPUT:", user_input)

    # ✅ 2. Load prompt
    prompt_template = Path("prompts/describe_prompt.txt").read_text()
    prompt = prompt_template.replace("{input}", user_input)

    # ✅ 3. Call AI
    ai_response = call_groq(prompt)

    print("RAW AI:", ai_response)

    # ✅ 4. Fallback (no crash system)
    if not ai_response:
        return jsonify({
            "analysis": {
                "category": "Unknown",
                "severity": "Medium",
                "summary": "Unable to analyze ESG risk at the moment.",
                "impact": {
                    "financial": "Potential financial implications require further review",
                    "legal": "Possible regulatory concerns",
                    "brand": "Reputational risks may exist"
                },
                "explanation": "Fallback response due to AI service unavailability"
            },
            "source": "fallback",
            "generated_at": datetime.utcnow().isoformat()
        })

    # ✅ 5. Extract JSON safely
    match = re.search(r"\{.*\}", ai_response, re.DOTALL)

    if not match:
        return jsonify({
            "error": "No valid JSON object found",
            "raw": ai_response
        }), 500

    try:
        cleaned_json = match.group()

        # Fix common AI issues
        cleaned_json = cleaned_json.replace(",}", "}").replace(",]", "]")

        result = json.loads(cleaned_json)

    except Exception as e:
        return jsonify({
            "error": "JSON parsing failed",
            "details": str(e),
            "raw": ai_response
        }), 500

    # ✅ 6. Validate structure
    required_keys = ["category", "severity", "summary", "impact", "explanation"]

    if not all(key in result for key in required_keys):
        return jsonify({
            "error": "Invalid AI response format",
            "raw": result
        }), 500

    # ✅ 7. Final response (PRO FORMAT)
    return jsonify({
        "analysis": result,
        "source": "ai",
        "generated_at": datetime.utcnow().isoformat()
    })