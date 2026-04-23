from flask import Blueprint, request, jsonify
from services.groq_client import generate_response
from services.security import sanitize_input, is_malicious

generate_bp = Blueprint("generate", __name__)


def load_prompt(E, S, G):
    with open("prompts/report_prompt.txt", "r", encoding="utf-8") as f:
        template = f.read()
    return template.format(E=E, S=S, G=G)


@generate_bp.route("/generate-report", methods=["POST"])
def generate_report():
    data = request.json or {}

    E = sanitize_input(data.get("E"))
    S = sanitize_input(data.get("S"))
    G = sanitize_input(data.get("G"))

    # security check
    if any(is_malicious(str(v)) for v in [E, S, G]):
        return jsonify({"error": "Malicious input detected"}), 400

    prompt = load_prompt(E, S, G)

    ai_response = generate_response(prompt)

    return jsonify({
        "data": ai_response,
        "generated_at": "now"
    })