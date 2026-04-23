from flask import Blueprint, request, jsonify
from services.groq_client import generate_response
from services.security import sanitize_input, is_malicious

generate_bp = Blueprint("generate", __name__)

@generate_bp.route("/generate-report", methods=["POST"])
def generate_report():
    data = request.json or {}

    # sanitize inputs
    E = sanitize_input(data.get("E"))
    S = sanitize_input(data.get("S"))
    G = sanitize_input(data.get("G"))

    # simple malicious check (if any text fields are added later)
    if any(is_malicious(str(v)) for v in [E, S, G]):
        return jsonify({"error": "Malicious input detected"}), 400

    prompt = f"""
    Analyze ESG data:
    Environmental: {E}
    Social: {S}
    Governance: {G}

    Provide:
    - Summary
    - Risks
    - Recommendations
    """

    ai_response = generate_response(prompt)

    return jsonify({
        "report": ai_response,
        "generated_at": "now"
    })