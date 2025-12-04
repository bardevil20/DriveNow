from datetime import datetime
from enum import Enum as PyEnum
from models import db


class CarStatus(PyEnum):
    """Enum for car status"""
    AVAILABLE = 'AVAILABLE'
    IN_USE = 'IN_USE'
    UNDER_MAINTENANCE = 'UNDER_MAINTENANCE'


class Cars(db.Model):
    """Car model"""
    __tablename__ = 'cars'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum(CarStatus), nullable=True)  # None = no status yet
    created_at = db.Column(db.DateTime, default=datetime.timezone.utc)
    
    def to_dict(self):
        return {
            'id': self.id,
            'model': self.model,
            'year': self.year,
            'status': self.status.value if self.status else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

