"""Unit tests for rental routes - testing HTTP status codes."""

import pytest
from unittest.mock import patch
from core.exceptions import NotFoundError, ValidationError, BusinessLogicError


class TestRegisterRentalRoute:
    """Tests for POST /api/rentals/register endpoint."""
    
    @patch('routes.rentals_routes.rentals_service')
    def test_register_rental_success(self, mock_service, client, mock_rental_data):
        """Test registering rental returns 201."""
        mock_service.register_rental.return_value = mock_rental_data
        
        response = client.post('/api/rentals/register', json={
            'car_id': '1',
            'customer_name': 'John Doe',
            'start_date': '20240101',
            'end_date': '20240105'
        })
        
        assert response.status_code == 201
        assert response.json == mock_rental_data
    
    def test_register_rental_no_data(self, client):
        """Test registering rental without data returns 400."""
        response = client.post('/api/rentals/register',
                               data='',
                               content_type='application/json')
        
        # Empty body returns 400 (Bad Request)
        assert response.status_code == 400
    
    @patch('routes.rentals_routes.rentals_service')
    def test_register_rental_validation_error(self, mock_service, client):
        """Test registering rental with missing fields returns 400."""
        mock_service.register_rental.side_effect = ValidationError(
            "Car ID, customer name, start date, and end date are required"
        )
        
        response = client.post('/api/rentals/register', json={'car_id': '1'})
        
        assert response.status_code == 400
        assert 'required' in response.json['error']
    
    @patch('routes.rentals_routes.rentals_service')
    def test_register_rental_car_not_found(self, mock_service, client):
        """Test registering rental for non-existent car returns 404."""
        mock_service.register_rental.side_effect = NotFoundError("Car not found")
        
        response = client.post('/api/rentals/register', json={
            'car_id': '999',
            'customer_name': 'John Doe',
            'start_date': '20240101',
            'end_date': '20240105'
        })
        
        assert response.status_code == 404
        assert 'Car not found' in response.json['error']
    
    @patch('routes.rentals_routes.rentals_service')
    def test_register_rental_car_not_available(self, mock_service, client):
        """Test registering rental for unavailable car returns 400."""
        mock_service.register_rental.side_effect = BusinessLogicError("Car is not available")
        
        response = client.post('/api/rentals/register', json={
            'car_id': '1',
            'customer_name': 'John Doe',
            'start_date': '20240101',
            'end_date': '20240105'
        })
        
        assert response.status_code == 400
        assert 'not available' in response.json['error']


class TestGetRentalsRoute:
    """Tests for GET /api/rentals/get_rentals endpoint."""
    
    @patch('routes.rentals_routes.rentals_service')
    def test_get_rentals_success(self, mock_service, client, mock_rental_data):
        """Test getting all rentals returns 200."""
        mock_service.get_all_rentals.return_value = [mock_rental_data]
        
        response = client.get('/api/rentals/get_rentals')
        
        assert response.status_code == 200
        assert response.json == [mock_rental_data]
    
    @patch('routes.rentals_routes.rentals_service')
    def test_get_rentals_empty(self, mock_service, client):
        """Test getting rentals when none exist returns 200 with empty list."""
        mock_service.get_all_rentals.return_value = []
        
        response = client.get('/api/rentals/get_rentals')
        
        assert response.status_code == 200
        assert response.json == []


class TestGetRentalRoute:
    """Tests for GET /api/rentals/<id> endpoint."""
    
    @patch('routes.rentals_routes.rentals_service')
    def test_get_rental_success(self, mock_service, client, mock_rental_data):
        """Test getting existing rental returns 200."""
        mock_service.get_rental.return_value = mock_rental_data
        
        response = client.get('/api/rentals/1')
        
        assert response.status_code == 200
        assert response.json == mock_rental_data
    
    @patch('routes.rentals_routes.rentals_service')
    def test_get_rental_not_found(self, mock_service, client):
        """Test getting non-existent rental returns 404."""
        mock_service.get_rental.side_effect = NotFoundError("Rental not found")
        
        response = client.get('/api/rentals/999')
        
        assert response.status_code == 404
        assert 'error' in response.json


class TestEndRentalRoute:
    """Tests for PUT /api/rentals/<id>/end endpoint."""
    
    @patch('routes.rentals_routes.rentals_service')
    def test_end_rental_success(self, mock_service, client, mock_rental_data):
        """Test ending rental returns 200."""
        mock_rental_data['completed'] = True
        mock_service.end_rental.return_value = mock_rental_data
        
        response = client.put('/api/rentals/1/end')
        
        assert response.status_code == 200
        assert response.json['completed'] is True
    
    @patch('routes.rentals_routes.rentals_service')
    def test_end_rental_not_found(self, mock_service, client):
        """Test ending non-existent rental returns 404."""
        mock_service.end_rental.side_effect = NotFoundError("Rental not found")
        
        response = client.put('/api/rentals/999/end')
        
        assert response.status_code == 404
        assert 'error' in response.json
    
    @patch('routes.rentals_routes.rentals_service')
    def test_end_rental_already_completed(self, mock_service, client):
        """Test ending already completed rental returns 400."""
        mock_service.end_rental.side_effect = BusinessLogicError("Rental already completed")
        
        response = client.put('/api/rentals/1/end')
        
        assert response.status_code == 400
        assert 'already completed' in response.json['error']


class TestDeleteRentalRoute:
    """Tests for DELETE /api/rentals/<id> endpoint."""
    
    @patch('routes.rentals_routes.rentals_service')
    def test_delete_rental_success(self, mock_service, client):
        """Test deleting rental returns 200."""
        mock_service.delete_rental.return_value = True
        
        response = client.delete('/api/rentals/1')
        
        assert response.status_code == 200
        assert 'deleted' in response.json['message']
    
    @patch('routes.rentals_routes.rentals_service')
    def test_delete_rental_not_found(self, mock_service, client):
        """Test deleting non-existent rental returns 404."""
        mock_service.delete_rental.side_effect = NotFoundError("Rental not found")
        
        response = client.delete('/api/rentals/999')
        
        assert response.status_code == 404
        assert 'error' in response.json
