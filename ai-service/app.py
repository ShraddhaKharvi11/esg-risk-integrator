from flask import Flask
from routes.generate import generate_bp

app = Flask(__name__)

app.register_blueprint(generate_bp)

@app.route("/")
def home():
    return "AI Service Running"

if __name__ == "__main__":
    app.run(port=5000, debug=True)