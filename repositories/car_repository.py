"""Car repository - handles all database operations for cars."""

from sqlalchemy import exists
from models import db, Cars as CarsModel, CarStatus


class CarRepository:
    
    def get_all(self):
        """Get all cars."""
        return CarsModel.query.all()
    
    def get_by_id(self, car_id):
        """Get a car by ID."""
        return CarsModel.query.get(car_id)
    
    def get_by_status(self, status):
        """Get all cars with a specific status (or None for no status)."""
        return CarsModel.query.filter_by(status=status).all()
    
    def get_by_model(self, model):
        """Get all cars by model name."""
        return CarsModel.query.filter_by(model=model).all()
    
    def get_by_year(self, year):
        """Get all cars by year."""
        return CarsModel.query.filter_by(year=year).all()
    
    def exists_by_model_and_year(self, model, year):
        """Check if a car with the given model and year exists."""
        return db.session.query(
            exists().where(CarsModel.model == model).where(CarsModel.year == year)
        ).scalar()
    
    def get_by_model_and_year(self, model, year):
        """Get a car by model and year."""
        return CarsModel.query.filter_by(model=model, year=year).first()
    
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
        """Set car status to AVAILABLE."""
        car = self.get_by_id(car_id)
        if not car:
            return None
        return self._update_status(car, CarStatus.AVAILABLE)
    
    def set_in_use(self, car_id):
        """Set car status to IN_USE."""
        car = self.get_by_id(car_id)
        if not car:
            return None
        return self._update_status(car, CarStatus.IN_USE)
    
    def set_under_maintenance(self, car_id):
        """Set car status to UNDER_MAINTENANCE."""
        car = self.get_by_id(car_id)
        if not car:
            return None
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

