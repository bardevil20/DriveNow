import logging
import os

from core.exceptions import AppException, NotFoundError, ValidationError, BusinessLogicError


def get_logger(name):
    """Get a logger"""
    return logging.getLogger(name)


def setup_logging():
    """Setup basic logging"""
    level = os.getenv('LOG_LEVEL', 'INFO')
    logging.basicConfig(
        level=getattr(logging, level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    # Quiet down werkzeug
    logging.getLogger('werkzeug').setLevel(logging.WARNING)

