from flask import Blueprint, request, jsonify
from services.groq_client import generate_response

generate_bp = Blueprint("generate", __name__)

@generate_bp.route("/generate-report", methods=["POST"])
def generate_report():
    data = request.json

    prompt = f"""
    Analyze the following ESG data and generate a report:
    
    Environmental Score: {data.get("E")}
    Social Score: {data.get("S")}
    Governance Score: {data.get("G")}
    
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