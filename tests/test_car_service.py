"""Unit tests for CarService."""

import pytest
from unittest.mock import MagicMock, patch
from services.car_service import CarService, parse_status
from models import CarStatus
from core.exceptions import NotFoundError, ValidationError, BusinessLogicError


class TestParseStatus:
    """Tests for parse_status helper function."""
    
    def test_parse_status_valid_available(self):
        """Test parsing valid AVAILABLE status."""
        result = parse_status('AVAILABLE')
        assert result == CarStatus.AVAILABLE
    
    def test_parse_status_valid_in_use(self):
        """Test parsing valid IN_USE status."""
        result = parse_status('in_use')  # lowercase
        assert result == CarStatus.IN_USE
    
    def test_parse_status_valid_under_maintenance(self):
        """Test parsing valid UNDER_MAINTENANCE status."""
        result = parse_status('Under_Maintenance')  # mixed case
        assert result == CarStatus.UNDER_MAINTENANCE
    
    def test_parse_status_invalid(self):
        """Test parsing invalid status raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            parse_status('INVALID_STATUS')
        assert "Invalid status" in str(exc_info.value.message)


class TestCarServiceGetCar:
    """Tests for CarService.get_car method."""
    
    @patch('services.car_service.CarRepository')
    def test_get_car_success(self, mock_repo_class, mock_car_model, mock_car_data):
        """Test getting a car that exists."""
        mock_repo = MagicMock()
        mock_repo.get_by_id.return_value = mock_car_model
        mock_repo_class.return_value = mock_repo
        
        service = CarService()
        result = service.get_car(1)
        
        assert result == mock_car_data
        mock_repo.get_by_id.assert_called_once_with(1)
    
    @patch('services.car_service.CarRepository')
    def test_get_car_not_found(self, mock_repo_class):
        """Test getting a car that doesn't exist raises NotFoundError."""
        mock_repo = MagicMock()
        mock_repo.get_by_id.return_value = None
        mock_repo_class.return_value = mock_repo
        
        service = CarService()
        
        with pytest.raises(NotFoundError) as exc_info:
            service.get_car(999)
        assert "Car not found" in str(exc_info.value.message)


class TestCarServiceGetAllCars:
    """Tests for CarService.get_all_cars method."""
    
    @patch('services.car_service.CarRepository')
    def test_get_all_cars_success(self, mock_repo_class, mock_car_model, mock_car_data):
        """Test getting all cars."""
        mock_repo = MagicMock()
        mock_repo.get_all.return_value = [mock_car_model]
        mock_repo_class.return_value = mock_repo
        
        service = CarService()
        result = service.get_all_cars()
        
        assert result == [mock_car_data]
        mock_repo.get_all.assert_called_once()
    
    @patch('services.car_service.CarRepository')
    def test_get_all_cars_empty(self, mock_repo_class):
        """Test getting all cars when none exist."""
        mock_repo = MagicMock()
        mock_repo.get_all.return_value = []
        mock_repo_class.return_value = mock_repo
        
        service = CarService()
        result = service.get_all_cars()
        
        assert result == []


class TestCarServiceCreateCar:
    """Tests for CarService.create_car method."""
    
    @patch('services.car_service.CarRepository')
    def test_create_car_success(self, mock_repo_class, mock_car_model, mock_car_data):
        """Test creating a car with valid data."""
        mock_repo = MagicMock()
        mock_repo.exists_by_model_and_year.return_value = False
        mock_repo.create.return_value = mock_car_model
        mock_repo_class.return_value = mock_repo
        
        service = CarService()
        result = service.create_car({'model': 'Toyota Camry', 'year': '2023'})
        
        assert result == mock_car_data
        mock_repo.create.assert_called_once_with('Toyota Camry', '2023')
    
    @patch('services.car_service.CarRepository')
    def test_create_car_missing_model(self, mock_repo_class):
        """Test creating a car without model raises ValidationError."""
        mock_repo_class.return_value = MagicMock()
        
        service = CarService()
        
        with pytest.raises(ValidationError) as exc_info:
            service.create_car({'year': '2023'})
        assert "Model and year are required" in str(exc_info.value.message)
    
    @patch('services.car_service.CarRepository')
    def test_create_car_missing_year(self, mock_repo_class):
        """Test creating a car without year raises ValidationError."""
        mock_repo_class.return_value = MagicMock()
        
        service = CarService()
        
        with pytest.raises(ValidationError) as exc_info:
            service.create_car({'model': 'Toyota Camry'})
        assert "Model and year are required" in str(exc_info.value.message)
    
    @patch('services.car_service.CarRepository')
    def test_create_car_invalid_year(self, mock_repo_class):
        """Test creating a car with invalid year raises ValidationError."""
        mock_repo_class.return_value = MagicMock()
        
        service = CarService()
        
        with pytest.raises(ValidationError) as exc_info:
            service.create_car({'model': 'Toyota Camry', 'year': 'invalid'})
        assert "Invalid year" in str(exc_info.value.message)
    
    @patch('services.car_service.CarRepository')
    def test_create_car_year_too_short(self, mock_repo_class):
        """Test creating a car with too short year raises ValidationError."""
        mock_repo_class.return_value = MagicMock()
        
        service = CarService()
        
        with pytest.raises(ValidationError) as exc_info:
            service.create_car({'model': 'Toyota Camry', 'year': '23'})
        assert "Invalid year" in str(exc_info.value.message)
    
    @patch('services.car_service.CarRepository')
    def test_create_car_duplicate(self, mock_repo_class):
        """Test creating a duplicate car raises BusinessLogicError."""
        mock_repo = MagicMock()
        mock_repo.exists_by_model_and_year.return_value = True
        mock_repo_class.return_value = mock_repo
        
        service = CarService()
        
        with pytest.raises(BusinessLogicError) as exc_info:
            service.create_car({'model': 'Toyota Camry', 'year': '2023'})
        assert "already exists" in str(exc_info.value.message)


class TestCarServiceUpdateStatus:
    """Tests for CarService.update_car_status method."""
    
    @patch('services.car_service.CarRepository')
    def test_update_status_success_string(self, mock_repo_class, mock_car_model, mock_car_data):
        """Test updating car status with string input."""
        mock_repo = MagicMock()
        mock_repo.set_available.return_value = mock_car_model
        mock_repo_class.return_value = mock_repo
        
        service = CarService()
        result = service.update_car_status(1, 'AVAILABLE')
        
        assert result == mock_car_data
        mock_repo.set_available.assert_called_once_with(1)
    
    @patch('services.car_service.CarRepository')
    def test_update_status_success_enum(self, mock_repo_class, mock_car_model, mock_car_data):
        """Test updating car status with enum input."""
        mock_repo = MagicMock()
        mock_repo.set_in_use.return_value = mock_car_model
        mock_repo_class.return_value = mock_repo
        
        service = CarService()
        result = service.update_car_status(1, CarStatus.IN_USE)
        
        assert result == mock_car_data
        mock_repo.set_in_use.assert_called_once_with(1)
    
    @patch('services.car_service.CarRepository')
    def test_update_status_car_not_found(self, mock_repo_class):
        """Test updating status of non-existent car raises NotFoundError."""
        mock_repo = MagicMock()
        mock_repo.set_available.return_value = None
        mock_repo_class.return_value = mock_repo
        
        service = CarService()
        
        with pytest.raises(NotFoundError) as exc_info:
            service.update_car_status(999, 'AVAILABLE')
        assert "Car not found" in str(exc_info.value.message)
    
    @patch('services.car_service.CarRepository')
    def test_update_status_invalid_status(self, mock_repo_class):
        """Test updating with invalid status raises ValidationError."""
        mock_repo_class.return_value = MagicMock()
        
        service = CarService()
        
        with pytest.raises(ValidationError) as exc_info:
            service.update_car_status(1, 'INVALID')
        assert "Invalid status" in str(exc_info.value.message)


class TestCarServiceDeleteCar:
    """Tests for CarService.delete_car method."""
    
    @patch('services.car_service.CarRepository')
    def test_delete_car_success_no_rental(self, mock_repo_class, mock_car_model):
        """Test deleting a car without active rental."""
        mock_repo = MagicMock()
        mock_repo.get_by_id.return_value = mock_car_model
        mock_repo.delete_by_id.return_value = True
        mock_repo_class.return_value = mock_repo
        
        service = CarService()
        # Mock the rental_service property
        service._rental_service = MagicMock()
        service._rental_service.get_active_rental_by_car.return_value = None
        
        result = service.delete_car(1)
        
        assert result is True
        mock_repo.delete_by_id.assert_called_once_with(1)
    
    @patch('services.car_service.CarRepository')
    def test_delete_car_not_found(self, mock_repo_class):
        """Test deleting non-existent car raises NotFoundError."""
        mock_repo = MagicMock()
        mock_repo.get_by_id.return_value = None
        mock_repo_class.return_value = mock_repo
        
        service = CarService()
        
        with pytest.raises(NotFoundError) as exc_info:
            service.delete_car(999)
        assert "Car not found" in str(exc_info.value.message)
    
    @patch('services.car_service.CarRepository')
    def test_delete_car_with_active_rental(self, mock_repo_class, mock_car_model, mock_rental_data):
        """Test deleting car completes active rental first."""
        mock_repo = MagicMock()
        mock_repo.get_by_id.return_value = mock_car_model
        mock_repo.delete_by_id.return_value = True
        mock_repo_class.return_value = mock_repo
        
        service = CarService()
        # Mock the rental_service
        service._rental_service = MagicMock()
        service._rental_service.get_active_rental_by_car.return_value = mock_rental_data
        service._rental_service.end_rental.return_value = mock_rental_data
        
        result = service.delete_car(1)
        
        assert result is True
        service._rental_service.end_rental.assert_called_once_with(mock_rental_data['rental_id'])
        mock_repo.delete_by_id.assert_called_once_with(1)
