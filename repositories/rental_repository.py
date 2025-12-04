"""Rental repository - handles all database operations for rentals."""

from datetime import datetime
from models import db, Rentals as RentalsModel, Cars as CarsModel


class RentalRepository:
    
    def __init__(self, car_repository):
        """Initialize with car repository for status updates."""
        self.car_repository = car_repository
    
    def get_all(self):
        """Get all rentals."""
        return RentalsModel.query.all()
    
    def get_by_id(self, rental_id):
        """Get a rental by ID."""
        return RentalsModel.query.get(rental_id)
    
    def get_by_car_id(self, car_id):
        """Get all rentals for a specific car."""
        return RentalsModel.query.filter_by(car_id=car_id).all()
    
    def get_by_customer(self, customer_name):
        """Get all rentals for a specific customer."""
        return RentalsModel.query.filter_by(customer_name=customer_name).all()
    
    def get_active_rentals(self):
        """Get all active rentals (cars currently in use)."""
        return RentalsModel.query.join(RentalsModel.car).filter(
            CarsModel.status==CarsModel.CarStatus.IN_USE.value
        ).all()
    
    def start_rental(self, car_id, customer_name, start_date, end_date):
        """
        Start a new rental and set car status to IN_USE.
        
        Args:
            car_id: The car ID to rent
            customer_name: The customer's name
            start_date: Rental start date
            end_date: Rental end date
            
        Returns:
            The created rental object
        """
        rental = RentalsModel(
            car_id=car_id,
            customer_name=customer_name,
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(rental)
        self.car_repository.set_in_use(car_id)
        db.session.commit()
        return rental
    
    def complete_rental(self, rental_id):
        """
        Complete a rental and set car status back to AVAILABLE.
        
        Args:
            rental_id: The rental ID to complete
            
        Returns:
            The updated rental object, or None if not found
        """
        rental = self.get_by_id(rental_id)
        if not rental:
            return None
        rental.completed = True
        rental.completed_at = datetime.now()
        self.car_repository.set_available(rental.car_id)
        return rental
    
    def _delete(self, rental):
        """Delete a rental."""
        db.session.delete(rental)
        db.session.commit()
    
    def delete_by_id(self, rental_id):
        """Delete a rental by ID."""
        rental = self.get_by_id(rental_id)
        if rental:
            self.car_repository.set_available(rental.car_id)
            self._delete(rental)
            return True
        return False

