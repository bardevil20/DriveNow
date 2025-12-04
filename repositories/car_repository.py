"""Car repository - handles all database operations for cars."""

from models import db, Cars as CarsModel, CarStatus


class CarRepository:
    
    def get_all(self):
        """Get all cars."""
        return CarsModel.query.all()
    
    def get_by_id(self, car_id):
        """Get a car by ID."""
        return CarsModel.query.get(car_id)
    
    def get_by_status(self, status):
        """Get all cars with a specific status."""
        return CarsModel.query.filter_by(status=status).all()
    
    def get_available(self):
        """Get all available cars."""
        return CarsModel.query.filter_by(status=CarStatus.AVAILABLE).all()
    
    def get_in_use(self):
        """Get all cars currently in use."""
        return CarsModel.query.filter_by(status=CarStatus.IN_USE).all()
    
    def get_under_maintenance(self):
        """Get all cars under maintenance."""
        return CarsModel.query.filter_by(status=CarStatus.UNDER_MAINTENANCE).all()
    
    def get_without_status(self):
        """Get all cars without a status yet."""
        return CarsModel.query.filter_by(status=None).all()
    
    # Managing vehicles: Add
    def create(self, model, year, status=None):
        """Add a new car."""
        car = CarsModel(model=model, year=year, status=status)
        db.session.add(car)
        db.session.commit()
        return car
    
    def _update_status(self, car: CarsModel, status: CarStatus):
        """Update a car's status. Internal use only."""
        car.status = status.value
        db.session.commit()
        return car
    
    def set_available(self, car_id):
        car = self.get_by_id(car_id)
        if not car:
            return None
        """Set car status to AVAILABLE."""
        return self._update_status(car, CarStatus.AVAILABLE)
    
    def set_in_use(self, car_id):
        car = self.get_by_id(car_id)
        if not car:
            return None
        """Set car status to IN_USE."""
        return self._update_status(car, CarStatus.IN_USE)
    
    def set_under_maintenance(self, car_id):
        car = self.get_by_id(car_id)
        if not car:
            return None
        """Set car status to UNDER_MAINTENANCE."""
        return self._update_status(car, CarStatus.UNDER_MAINTENANCE)
    
    # Managing vehicles: Delete
    def _delete(self, car):
        """Delete a car. Internal use only."""
        db.session.delete(car)
        db.session.commit()
    
    def delete_by_id(self, car_id):
        """Delete a car by ID."""
        car = self.get_by_id(car_id)
        if car:
            self._delete(car)
            return True
        return False

