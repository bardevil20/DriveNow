from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models here so they're registered with SQLAlchemy
from models.cars import Cars
from models.cars import CarStatus
from models.rentals import Rentals
