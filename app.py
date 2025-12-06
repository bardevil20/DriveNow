from flask import Flask
import mysql.connector
from mysql.connector import Error
from config import Config
from core import setup_logging, get_logger
from routes import cars_bp, rentals_bp
from models import db

setup_logging()
logger = get_logger(__name__)


def ensure_database_exists():
    """Check if database exists and create it if not."""
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DATABASE}")
        logger.info(f"Database '{Config.MYSQL_DATABASE}' is ready")
        cursor.close()
        connection.close()
    except Error as e:
        logger.error(f"Error connecting to MySQL: {e}")
        raise


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    app.register_blueprint(cars_bp)
    app.register_blueprint(rentals_bp)

    return app


def init_db(app):
    """Initialize database and create tables if they don't exist."""
    with app.app_context():
        db.create_all()
        logger.info("Database tables are ready")


app = create_app()

if __name__ == '__main__':
    ensure_database_exists()
    init_db(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
