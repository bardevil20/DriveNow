"""Car service - business logic for car operations."""

import logging
from repositories import CarRepository
from models import CarStatus

logger = logging.getLogger(__name__)


class CarService:
    
    def __init__(self):
        self.repo = CarRepository()
    
    def get_all_cars(self):
        cars = self.repo.get_all()
        logger.info(f"Fetched {len(cars)} cars")
        return [c.to_dict() for c in cars]

    def get_car(self, car_id):
        car = self.repo.get_by_id(car_id)
        if not car:
            return None, "Car not found"
        return car.to_dict(), None

    def get_cars_by_model(self, model):
        cars = self.repo.get_by_model(model)
        if not cars:
            return None, "No cars found with this model"
        return [c.to_dict() for c in cars], None

    def get_cars_by_year(self, year):
        cars = self.repo.get_by_year(year)
        if not cars:
            return None, "No cars found with this year"
        return [c.to_dict() for c in cars], None
    
    def _get_cars_by_status(self, status):
        cars = self.repo.get_by_status(status)
        if not cars:
            return None, "No cars found with this status"
        return [c.to_dict() for c in cars], None

    def get_available_cars(self):
        cars = self._get_cars_by_status(CarStatus.AVAILABLE)
        if not cars:
            return None, "No available cars found"
        return [c.to_dict() for c in cars], None

    def get_in_use_cars(self):
        cars = self._get_cars_by_status(CarStatus.IN_USE)
        if not cars:
            return None, "No in use cars found"
        return [c.to_dict() for c in cars], None

    def get_under_maintenance_cars(self):
        cars = self._get_cars_by_status(CarStatus.UNDER_MAINTENANCE)
        if not cars:
            return None, "No under maintenance cars found"
        return [c.to_dict() for c in cars], None

    def get_without_status_cars(self):
        cars = self._get_cars_by_status(None)
        if not cars:
            return None, "No cars without status found"
        return [c.to_dict() for c in cars], None

    def create_car(self, data):
        # Validate
        if not data:
            return None, "No data provided"
        
        model = data.get('model', '').strip()
        year = data.get('year', '').strip().lower()
        
        if not model or not year:
            return None, "Model and year are required"
        
        car = self.repo.create(model, year)
        logger.info(f"Created car: {car.id}")
        return car.to_dict(), None
    