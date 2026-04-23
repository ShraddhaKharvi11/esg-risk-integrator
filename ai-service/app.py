from flask import Flask
from routes.describe import describe_bp

app = Flask(__name__)

app.register_blueprint(describe_bp)

@app.route('/health')
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    app.run(port=5000, debug=True)