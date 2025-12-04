"""Rental repository - handles all database operations for rentals."""

from models import db, Rentals as RentalsModel, Cars as CarsModel


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
    
    def get_active_rentals(self):
        """Get all active rentals (cars currently in use)."""
        return RentalsModel.query.join(RentalsModel.car).filter(
            CarsModel.status==CarsModel.CarStatus.IN_USE.value
        ).all()
    
    def complete_rental(self, rental):
        """
        Complete a rental and set car status back to AVAILABLE.
        
        Args:
            rental: The rental object to complete
            
        Returns:
            The updated rental object
        """
        rental.car.status = CarsModel.CarStatus.AVAILABLE
        db.session.commit()
        return rental
    
    def delete(self, rental):
        """Delete a rental."""
        db.session.delete(rental)
        db.session.commit()
    
    def delete_by_id(self, rental_id):
        """Delete a rental by ID."""
        rental = self.get_by_id(rental_id)
        if rental:
            self.delete(rental)
            return True
        return False

