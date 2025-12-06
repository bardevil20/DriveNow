"""Car service - business logic for car operations."""

import logging
from repositories import CarRepository
from models import CarStatus
from core.exceptions import NotFoundError, ValidationError, BusinessLogicError

logger = logging.getLogger(__name__)

# Maps CarStatus to the corresponding repository method name
STATUS_METHOD_MAP = {
    CarStatus.AVAILABLE: 'set_available',
    CarStatus.IN_USE: 'set_in_use',
    CarStatus.UNDER_MAINTENANCE: 'set_under_maintenance',
}


def parse_status(status_str: str) -> CarStatus:
    """Convert status string to CarStatus enum."""
    try:
        return CarStatus[status_str.upper()]
    except KeyError:
        valid_statuses = [s.name for s in CarStatus]
        raise ValidationError(f"Invalid status. Valid values: {valid_statuses}")


class CarService:
    
    def __init__(self):
        self.repo = CarRepository()
        self._rental_service = None
    
    @property
    def rental_service(self):
        """Lazy import to avoid circular dependency."""
        if self._rental_service is None:
            from services.rental_service import RentalService
            self._rental_service = RentalService()
        return self._rental_service
    
    def get_all_cars(self):
        """Get all cars."""
        cars = self.repo.get_all()
        return [c.to_dict() for c in cars]

    def get_car(self, car_id):
        """Get a car by ID."""
        car = self.repo.get_by_id(car_id)
        if not car:
            raise NotFoundError("Car not found")
        return car.to_dict()

    def get_cars_by_model(self, model):
        """Get cars by model."""
        cars = self.repo.get_by_model(model)
        if not cars:
            raise NotFoundError("No cars found with this model")
        return [c.to_dict() for c in cars]

    def get_cars_by_year(self, year):
        """Get cars by year."""
        cars = self.repo.get_by_year(year)
        if not cars:
            raise NotFoundError("No cars found with this year")
        return [c.to_dict() for c in cars]
    
    def _get_cars_by_status(self, status):
        """Get cars by status."""
        cars = self.repo.get_by_status(status)
        return [c.to_dict() for c in cars]

    def get_available_cars(self):
        """Get available cars."""
        return self._get_cars_by_status(CarStatus.AVAILABLE)

    def get_in_use_cars(self):
        """Get cars in use."""
        return self._get_cars_by_status(CarStatus.IN_USE)

    def get_under_maintenance_cars(self):
        """Get cars under maintenance."""
        return self._get_cars_by_status(CarStatus.UNDER_MAINTENANCE)

    def get_without_status_cars(self):
        """Get cars without status."""
        return self._get_cars_by_status(None)

    def create_car(self, data):
        """Create a new car."""
        model = data.get('model', '').strip() if data.get('model') else ''
        year = data.get('year', '').strip() if data.get('year') else ''
        
        if not model or not year:
            raise ValidationError("Model and year are required")

        if not self._is_valid_year(year):
            raise ValidationError("Invalid year number")
        
        if self._is_model_and_year_exists(model, year):
            raise BusinessLogicError("Model and year already exists")
        
        car = self.repo.create(model, year)
        return car.to_dict()
    
    def update_car_status(self, car_id, status_input):
        """
        Update a car's status using the appropriate repository method.
        
        Args:
            car_id: The car ID to update
            status_input: The status string or CarStatus enum
        """
        # Convert string to enum if needed
        if isinstance(status_input, str):
            status = parse_status(status_input)
        else:
            status = status_input
        
        method_name = STATUS_METHOD_MAP.get(status)
        if not method_name:
            raise ValidationError(f"Invalid status: {status}")
        
        method = getattr(self.repo, method_name)
        car = method(car_id)
        if not car:
            raise NotFoundError("Car not found")
        
        return car.to_dict()

    def delete_car(self, car_id):
        """Delete a car by ID. Completes active rental if exists."""
        # Check if car exists first
        car = self.repo.get_by_id(car_id)
        if not car:
            raise NotFoundError("Car not found")
        
        # Complete active rental if car is in use
        active_rental = self.rental_service.get_active_rental_by_car(car_id)
        if active_rental:
            self.rental_service.end_rental(active_rental['rental_id'])
        
        self.repo.delete_by_id(car_id)
        return True

    def _is_valid_year(self, year):
        return year.isdigit() and len(year) == 4 and int(year) > 1900

    def _is_model_and_year_exists(self, model, year):
        return self.repo.exists_by_model_and_year(model, year)
    