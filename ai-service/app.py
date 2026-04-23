from flask import Flask
from routes.generate import generate_bp
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# limit: 30 requests per minute
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute"]
)

app.register_blueprint(generate_bp)

@app.route("/")
def home():
    return "AI Service Running"

if __name__ == "__main__":
    app.run(port=5000, debug=True)