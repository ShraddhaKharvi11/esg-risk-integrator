from flask import Flask
from routes.generate import generate_bp
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Global rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["30 per minute"]
)

# Register blueprint
app.register_blueprint(generate_bp)


@app.route("/")
def home():
    return "AI Service Running"


if __name__ == "__main__":
    app.run(debug=True, port=5000)