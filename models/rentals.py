from datetime import datetime
from models import db


class Rentals(db.Model):
    """Rental model"""
    __tablename__ = 'rentals'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.timezone.utc)
    
    car = db.relationship('Cars', backref='rentals')

    def to_dict(self):
        return {
            'rental_id': self.id,
            'car_id': self.car.id,
            'car_model': self.car.model,
            'car_year': self.car.year,
            'car_status': self.car.status.value if self.car.status else None,
            'customer_name': self.customer_name,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'completed': self.completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
