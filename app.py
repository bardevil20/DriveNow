from flask import Flask
from config import Config
from core import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    app.register_blueprint(user_bp)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
