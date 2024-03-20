from flask import Flask
from flask_cors import CORS
from backend.api import api_bp
from backend.routes import routes_bp

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*", "methods": "GET, POST"}})
app.register_blueprint(api_bp)
app.register_blueprint(routes_bp)


if __name__ == '__main__':
    app.run(debug = True)