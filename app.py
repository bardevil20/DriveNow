from flask import Flask
from config import Config
from core import setup_logging, get_logger
from routes import cars_bp, rentals_bp
from models import db

setup_logging()
logger = get_logger(__name__)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    app.register_blueprint(cars_bp)
    app.register_blueprint(rentals_bp)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
