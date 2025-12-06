"""Shared test fixtures and configuration."""

import pytest
from unittest.mock import MagicMock
from app import create_app
from models import CarStatus


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_car_data():
    """Sample car data for testing."""
    return {
        'id': 1,
        'model': 'Toyota Camry',
        'year': 2023,
        'status': 'AVAILABLE',
        'created_at': '2024-01-01T00:00:00'
    }


@pytest.fixture
def mock_car_model(mock_car_data):
    """Mock car model object."""
    car = MagicMock()
    car.id = mock_car_data['id']
    car.model = mock_car_data['model']
    car.year = mock_car_data['year']
    car.status = CarStatus.AVAILABLE
    car.to_dict.return_value = mock_car_data
    return car


@pytest.fixture
def mock_rental_data():
    """Sample rental data for testing."""
    return {
        'rental_id': 1,
        'car_id': 1,
        'car_model': 'Toyota Camry',
        'car_year': 2023,
        'car_status': 'IN_USE',
        'customer_name': 'John Doe',
        'start_date': '2024-01-01T00:00:00',
        'end_date': '2024-01-05T00:00:00',
        'completed': False,
        'completed_at': None,
        'created_at': '2024-01-01T00:00:00'
    }


@pytest.fixture
def mock_rental_model(mock_rental_data):
    """Mock rental model object."""
    rental = MagicMock()
    rental.id = mock_rental_data['rental_id']
    rental.car_id = mock_rental_data['car_id']
    rental.customer_name = mock_rental_data['customer_name']
    rental.completed = False
    rental.to_dict.return_value = mock_rental_data
    return rental
