import os

from flask import Config, Flask
from flask_cors import CORS

from routes.record_route import record_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(record_bp)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000, debug = True)


