"""Unit tests for car routes - testing HTTP status codes."""

import pytest
from unittest.mock import patch, MagicMock
from core.exceptions import NotFoundError, ValidationError, BusinessLogicError


class TestCreateCarRoute:
    """Tests for POST /api/cars endpoint."""
    
    @patch('routes.car_routes.cars_service')
    def test_create_car_success(self, mock_service, client, mock_car_data):
        """Test creating car returns 201."""
        mock_service.create_car.return_value = mock_car_data
        
        response = client.post('/api/cars', 
                               json={'model': 'Toyota Camry', 'year': '2023'})
        
        assert response.status_code == 201
        assert response.json == mock_car_data
    
    def test_create_car_no_data(self, client):
        """Test creating car without data returns 400."""
        response = client.post('/api/cars', 
                               data='',
                               content_type='application/json')
        
        # Empty body returns 400 (Bad Request)
        assert response.status_code == 400
    
    @patch('routes.car_routes.cars_service')
    def test_create_car_validation_error(self, mock_service, client):
        """Test creating car with invalid data returns 400."""
        mock_service.create_car.side_effect = ValidationError("Model and year are required")
        
        response = client.post('/api/cars', json={'model': ''})
        
        assert response.status_code == 400
        assert 'error' in response.json
    
    @patch('routes.car_routes.cars_service')
    def test_create_car_duplicate(self, mock_service, client):
        """Test creating duplicate car returns 400."""
        mock_service.create_car.side_effect = BusinessLogicError("Model and year already exists")
        
        response = client.post('/api/cars', 
                               json={'model': 'Toyota Camry', 'year': '2023'})
        
        assert response.status_code == 400
        assert 'already exists' in response.json['error']


class TestGetCarsRoute:
    """Tests for GET /api/cars/get_cars endpoint."""
    
    @patch('routes.car_routes.cars_service')
    def test_get_cars_success(self, mock_service, client, mock_car_data):
        """Test getting all cars returns 200."""
        mock_service.get_all_cars.return_value = [mock_car_data]
        
        response = client.get('/api/cars/get_cars')
        
        assert response.status_code == 200
        assert response.json == [mock_car_data]
    
    @patch('routes.car_routes.cars_service')
    def test_get_cars_empty(self, mock_service, client):
        """Test getting cars when none exist returns 200 with empty list."""
        mock_service.get_all_cars.return_value = []
        
        response = client.get('/api/cars/get_cars')
        
        assert response.status_code == 200
        assert response.json == []


class TestGetCarRoute:
    """Tests for GET /api/cars/<id> endpoint."""
    
    @patch('routes.car_routes.cars_service')
    def test_get_car_success(self, mock_service, client, mock_car_data):
        """Test getting existing car returns 200."""
        mock_service.get_car.return_value = mock_car_data
        
        response = client.get('/api/cars/1')
        
        assert response.status_code == 200
        assert response.json == mock_car_data
    
    @patch('routes.car_routes.cars_service')
    def test_get_car_not_found(self, mock_service, client):
        """Test getting non-existent car returns 404."""
        mock_service.get_car.side_effect = NotFoundError("Car not found")
        
        response = client.get('/api/cars/999')
        
        assert response.status_code == 404
        assert 'error' in response.json


class TestUpdateCarStatusRoute:
    """Tests for PUT /api/cars/<id>/status endpoint."""
    
    @patch('routes.car_routes.cars_service')
    def test_update_status_success(self, mock_service, client, mock_car_data):
        """Test updating car status returns 200."""
        mock_car_data['status'] = 'IN_USE'
        mock_service.update_car_status.return_value = mock_car_data
        
        response = client.put('/api/cars/1/status', json={'status': 'IN_USE'})
        
        assert response.status_code == 200
        assert response.json['status'] == 'IN_USE'
    
    def test_update_status_no_data(self, client):
        """Test updating status without data returns 400."""
        response = client.put('/api/cars/1/status',
                              data='',
                              content_type='application/json')
        
        # Empty body returns 400 (Bad Request)
        assert response.status_code == 400
    
    def test_update_status_missing_status(self, client):
        """Test updating status without status field returns 400."""
        response = client.put('/api/cars/1/status', json={'other': 'value'})
        
        assert response.status_code == 400
        assert 'Status is required' in response.json['error']
    
    @patch('routes.car_routes.cars_service')
    def test_update_status_invalid(self, mock_service, client):
        """Test updating with invalid status returns 400."""
        mock_service.update_car_status.side_effect = ValidationError("Invalid status")
        
        response = client.put('/api/cars/1/status', json={'status': 'INVALID'})
        
        assert response.status_code == 400
        assert 'error' in response.json
    
    @patch('routes.car_routes.cars_service')
    def test_update_status_car_not_found(self, mock_service, client):
        """Test updating non-existent car returns 404."""
        mock_service.update_car_status.side_effect = NotFoundError("Car not found")
        
        response = client.put('/api/cars/999/status', json={'status': 'AVAILABLE'})
        
        assert response.status_code == 404
        assert 'error' in response.json


class TestDeleteCarRoute:
    """Tests for DELETE /api/cars/<id> endpoint."""
    
    @patch('routes.car_routes.cars_service')
    def test_delete_car_success(self, mock_service, client):
        """Test deleting car returns 200."""
        mock_service.delete_car.return_value = True
        
        response = client.delete('/api/cars/1')
        
        assert response.status_code == 200
        assert 'deleted' in response.json['message']
    
    @patch('routes.car_routes.cars_service')
    def test_delete_car_not_found(self, mock_service, client):
        """Test deleting non-existent car returns 404."""
        mock_service.delete_car.side_effect = NotFoundError("Car not found")
        
        response = client.delete('/api/cars/999')
        
        assert response.status_code == 404
        assert 'error' in response.json
