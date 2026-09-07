import os
from flask import Flask

try:
    from app import app
except ImportError:
    try:
        from main import app
    except ImportError:
        app = Flask(__name__)

        @app.route('/')
        def home():
            return "<h1>Serveur CF Montréal Chat en ligne !</h1>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
