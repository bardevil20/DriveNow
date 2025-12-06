"""Rental repository - handles all database operations for rentals."""

from datetime import datetime
from models import db, Rentals as RentalsModel


class RentalRepository:
    
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
    
    def get_active_by_car_id(self, car_id):
        """Get active (not completed) rental for a specific car."""
        return RentalsModel.query.filter_by(car_id=car_id, completed=False).first()
    
    def create(self, car_id, customer_name, start_date, end_date):
        """
        Create a new rental record.
        
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
        db.session.commit()
        return rental
    
    def complete_rental(self, rental_id):
        """
        Complete a rental.
        
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
        db.session.commit()
        return rental
    
    def _delete(self, rental):
        """Delete a rental."""
        db.session.delete(rental)
        db.session.commit()
    
    def delete_by_id(self, rental_id):
        """Delete a rental by ID."""
        rental = self.get_by_id(rental_id)
        if rental:
            self._delete(rental)
            return True
        return False

