"""Rental service - business logic for rental operations."""

import logging
from repositories import RentalRepository
from models import CarStatus

logger = logging.getLogger(__name__)


class RentalService:
    
    def __init__(self):
        self.repo = RentalRepository()
    
    def get_all_rentals(self):
        rentals = self.repo.get_all()
        logger.info(f"Fetched {len(rentals)} rentals")
        return [r.to_dict() for r in rentals]

    def get_rental(self, rental_id):
        rental = self.repo.get_by_id(rental_id)
        if not rental:
            return None, "Rental not found"
        return rental.to_dict(), None


    def register_rental(self, data):
        # Validate
        if not data:
            return None, "No data provided"
        
        car_id = data.get('car_id', '').strip()
        customer_name = data.get('customer_name', '').strip()
        start_date = data.get('start_date', '').strip()
        end_date = data.get('end_date', '').strip()
        
        if not car_id or not customer_name or not start_date or not end_date:
            return None, "Car ID, customer name, start date, and end date are required"

        car = self.repo.car_repository.get_by_id(car_id)
        if not car:
            return None, "Car not found"
        if car.status != CarStatus.AVAILABLE:
            return None, "Car is not available"
        
        valid, error = self._is_valid_dates(start_date, end_date)
        if not valid:
            return None, error
        
        rental = self.repo.start_rental(car_id, customer_name, start_date, end_date)
        logger.info(f"Registered rental: {rental.id}")
        return rental.to_dict(), None

    def end_rental(self, rental_id):
        rental = self.repo.get_by_id(rental_id)
        if not rental:
            return None, "Rental not found"
        if rental.completed:
            return None, "Rental already completed"
        rental = self.repo.complete_rental(rental_id)
        logger.info(f"Completed rental: {rental.id}")
        return rental.to_dict(), None

    def _is_valid_dates(self, start_date, end_date):
        if not self._is_valid_date(start_date):
            return False, "Invalid start date"
        if not self._is_valid_date(end_date):
            return False, "Invalid end date"
        if not self._is_valid_date_range(start_date, end_date):
            return False, "Start date must be before end date"
        return True
    
    def _is_valid_date(self, date):
        return date.isdigit() and len(date) == 8 and int(date) > 1900
    
    def _is_valid_date_range(self, start_date, end_date):
        return start_date < end_date
 