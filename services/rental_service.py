"""Rental service - business logic for rental operations."""

import logging
from repositories import RentalRepository
from repositories.car_repository import CarRepository
from models import CarStatus
from core.exceptions import NotFoundError, ValidationError, BusinessLogicError

logger = logging.getLogger(__name__)


class RentalService:
    
    def __init__(self):
        self.repo = RentalRepository()
        self.car_repo = CarRepository()
    
    def get_all_rentals(self):
        """Get all rentals."""
        rentals = self.repo.get_all()
        return [r.to_dict() for r in rentals]

    def get_rental(self, rental_id):
        """Get a rental by ID."""
        rental = self.repo.get_by_id(rental_id)
        if not rental:
            raise NotFoundError("Rental not found")
        return rental.to_dict()

    def register_rental(self, data):
        """Register a new rental."""
        # Validate required fields
        car_id = data.get('car_id', '').strip() if data.get('car_id') else ''
        customer_name = data.get('customer_name', '').strip() if data.get('customer_name') else ''
        start_date = data.get('start_date', '').strip() if data.get('start_date') else ''
        end_date = data.get('end_date', '').strip() if data.get('end_date') else ''
        
        if not car_id or not customer_name or not start_date or not end_date:
            raise ValidationError("Car ID, customer name, start date, and end date are required")

        # Business logic: check car exists and is available
        car = self.car_repo.get_by_id(car_id)
        if not car:
            raise NotFoundError("Car not found")
        if car.status != CarStatus.AVAILABLE:
            raise BusinessLogicError("Car is not available")
        
        # Validate dates
        self._validate_dates(start_date, end_date)
        
        # Create rental and update car status
        rental = self.repo.create(car_id, customer_name, start_date, end_date)
        self.car_repo.set_in_use(car_id)
        
        return rental.to_dict()

    def end_rental(self, rental_id):
        """End/complete a rental."""
        rental = self.repo.get_by_id(rental_id)
        if not rental:
            raise NotFoundError("Rental not found")
        if rental.completed:
            raise BusinessLogicError("Rental already completed")
        
        # Complete rental and set car to available
        rental = self.repo.complete_rental(rental_id)
        self.car_repo.set_available(rental.car_id)
        
        return rental.to_dict()

    def _validate_dates(self, start_date, end_date):
        """Validate rental dates."""
        if not self._is_valid_date(start_date):
            raise ValidationError("Invalid start date format (expected YYYYMMDD)")
        if not self._is_valid_date(end_date):
            raise ValidationError("Invalid end date format (expected YYYYMMDD)")
        if not self._is_valid_date_range(start_date, end_date):
            raise ValidationError("Start date must be before end date")
    
    def _is_valid_date(self, date):
        return date.isdigit() and len(date) == 8 and int(date[:4]) > 1900
    
    def _is_valid_date_range(self, start_date, end_date):
        return start_date < end_date

    def get_active_rental_by_car(self, car_id):
        """Get active (not completed) rental for a car. Returns None if not found."""
        rental = self.repo.get_active_by_car_id(car_id)
        if rental:
            return rental.to_dict()
        return None

    def delete_rental(self, rental_id):
        """Delete a rental. Sets car to AVAILABLE if rental was active."""
        rental = self.repo.get_by_id(rental_id)
        if not rental:
            raise NotFoundError("Rental not found")
        
        car_id = rental.car_id
        was_active = not rental.completed
        
        self.repo.delete_by_id(rental_id)
        
        # Set car to available if rental was active
        if was_active:
            self.car_repo.set_available(car_id)
        
        return True
 