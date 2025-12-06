"""Unit tests for RentalService."""

import pytest
from unittest.mock import MagicMock, patch
from services.rental_service import RentalService
from models import CarStatus
from core.exceptions import NotFoundError, ValidationError, BusinessLogicError


class TestRentalServiceGetRental:
    """Tests for RentalService.get_rental method."""
    
    @patch('services.rental_service.CarRepository')
    @patch('services.rental_service.RentalRepository')
    def test_get_rental_success(self, mock_rental_repo_class, mock_car_repo_class, 
                                 mock_rental_model, mock_rental_data):
        """Test getting a rental that exists."""
        mock_rental_repo = MagicMock()
        mock_rental_repo.get_by_id.return_value = mock_rental_model
        mock_rental_repo_class.return_value = mock_rental_repo
        mock_car_repo_class.return_value = MagicMock()
        
        service = RentalService()
        result = service.get_rental(1)
        
        assert result == mock_rental_data
        mock_rental_repo.get_by_id.assert_called_once_with(1)
    
    @patch('services.rental_service.CarRepository')
    @patch('services.rental_service.RentalRepository')
    def test_get_rental_not_found(self, mock_rental_repo_class, mock_car_repo_class):
        """Test getting a rental that doesn't exist raises NotFoundError."""
        mock_rental_repo = MagicMock()
        mock_rental_repo.get_by_id.return_value = None
        mock_rental_repo_class.return_value = mock_rental_repo
        mock_car_repo_class.return_value = MagicMock()
        
        service = RentalService()
        
        with pytest.raises(NotFoundError) as exc_info:
            service.get_rental(999)
        assert "Rental not found" in str(exc_info.value.message)


class TestRentalServiceGetAllRentals:
    """Tests for RentalService.get_all_rentals method."""
    
    @patch('services.rental_service.CarRepository')
    @patch('services.rental_service.RentalRepository')
    def test_get_all_rentals_success(self, mock_rental_repo_class, mock_car_repo_class,
                                      mock_rental_model, mock_rental_data):
        """Test getting all rentals."""
        mock_rental_repo = MagicMock()
        mock_rental_repo.get_all.return_value = [mock_rental_model]
        mock_rental_repo_class.return_value = mock_rental_repo
        mock_car_repo_class.return_value = MagicMock()
        
        service = RentalService()
        result = service.get_all_rentals()
        
        assert result == [mock_rental_data]
    
    @patch('services.rental_service.CarRepository')
    @patch('services.rental_service.RentalRepository')
    def test_get_all_rentals_empty(self, mock_rental_repo_class, mock_car_repo_class):
        """Test getting all rentals when none exist."""
        mock_rental_repo = MagicMock()
        mock_rental_repo.get_all.return_value = []
        mock_rental_repo_class.return_value = mock_rental_repo
        mock_car_repo_class.return_value = MagicMock()
        
        service = RentalService()
        result = service.get_all_rentals()
        
        assert result == []


class TestRentalServiceRegisterRental:
    """Tests for RentalService.register_rental method."""
    
    @patch('services.rental_service.CarRepository')
    @patch('services.rental_service.RentalRepository')
    def test_register_rental_success(self, mock_rental_repo_class, mock_car_repo_class,
                                      mock_rental_model, mock_rental_data, mock_car_model):
        """Test registering a rental with valid data."""
        mock_rental_repo = MagicMock()
        mock_rental_repo.create.return_value = mock_rental_model
        mock_rental_repo_class.return_value = mock_rental_repo
        
        mock_car_repo = MagicMock()
        mock_car_model.status = CarStatus.AVAILABLE
        mock_car_repo.get_by_id.return_value = mock_car_model
        mock_car_repo_class.return_value = mock_car_repo
        
        service = RentalService()
        result = service.register_rental({
            'car_id': '1',
            'customer_name': 'John Doe',
            'start_date': '20240101',
            'end_date': '20240105'
        })
        
        assert result == mock_rental_data
        mock_car_repo.set_in_use.assert_called_once_with('1')
    
    @patch('services.rental_service.CarRepository')
    @patch('services.rental_service.RentalRepository')
    def test_register_rental_missing_car_id(self, mock_rental_repo_class, mock_car_repo_class):
        """Test registering rental without car_id raises ValidationError."""
        mock_rental_repo_class.return_value = MagicMock()
        mock_car_repo_class.return_value = MagicMock()
        
        service = RentalService()
        
        with pytest.raises(ValidationError) as exc_info:
            service.register_rental({
                'customer_name': 'John Doe',
                'start_date': '20240101',
                'end_date': '20240105'
            })
        assert "required" in str(exc_info.value.message)
    
    @patch('services.rental_service.CarRepository')
    @patch('services.rental_service.RentalRepository')
    def test_register_rental_missing_customer_name(self, mock_rental_repo_class, mock_car_repo_class):
        """Test registering rental without customer_name raises ValidationError."""
        mock_rental_repo_class.return_value = MagicMock()
        mock_car_repo_class.return_value = MagicMock()
        
        service = RentalService()
        
        with pytest.raises(ValidationError) as exc_info:
            service.register_rental({
                'car_id': '1',
                'start_date': '20240101',
                'end_date': '20240105'
            })
        assert "required" in str(exc_info.value.message)
    
    @patch('services.rental_service.CarRepository')
    @patch('services.rental_service.RentalRepository')
    def test_register_rental_car_not_found(self, mock_rental_repo_class, mock_car_repo_class):
        """Test registering rental for non-existent car raises NotFoundError."""
        mock_rental_repo_class.return_value = MagicMock()
        
        mock_car_repo = MagicMock()
        mock_car_repo.get_by_id.return_value = None
        mock_car_repo_class.return_value = mock_car_repo
        
        service = RentalService()
        
        with pytest.raises(NotFoundError) as exc_info:
            service.register_rental({
                'car_id': '999',
                'customer_name': 'John Doe',
                'start_date': '20240101',
                'end_date': '20240105'
            })
        assert "Car not found" in str(exc_info.value.message)
    
    @patch('services.rental_service.CarRepository')
    @patch('services.rental_service.RentalRepository')
    def test_register_rental_car_not_available(self, mock_rental_repo_class, mock_car_repo_class,
                                                mock_car_model):
        """Test registering rental for unavailable car raises BusinessLogicError."""
        mock_rental_repo_class.return_value = MagicMock()
        
        mock_car_repo = MagicMock()
        mock_car_model.status = CarStatus.IN_USE
        mock_car_repo.get_by_id.return_value = mock_car_model
        mock_car_repo_class.return_value = mock_car_repo
        
        service = RentalService()
        
        with pytest.raises(BusinessLogicError) as exc_info:
            service.register_rental({
                'car_id': '1',
                'customer_name': 'John Doe',
                'start_date': '20240101',
                'end_date': '20240105'
            })
        assert "not available" in str(exc_info.value.message)
    
    @patch('services.rental_service.CarRepository')
    @patch('services.rental_service.RentalRepository')
    def test_register_rental_invalid_start_date(self, mock_rental_repo_class, mock_car_repo_class,
                                                 mock_car_model):
        """Test registering rental with invalid start date raises ValidationError."""
        mock_rental_repo_class.return_value = MagicMock()
        
        mock_car_repo = MagicMock()
        mock_car_model.status = CarStatus.AVAILABLE
        mock_car_repo.get_by_id.return_value = mock_car_model
        mock_car_repo_class.return_value = mock_car_repo
        
        service = RentalService()
        
        with pytest.raises(ValidationError) as exc_info:
            service.register_rental({
                'car_id': '1',
                'customer_name': 'John Doe',
                'start_date': 'invalid',
                'end_date': '20240105'
            })
        assert "Invalid start date" in str(exc_info.value.message)
    
    @patch('services.rental_service.CarRepository')
    @patch('services.rental_service.RentalRepository')
    def test_register_rental_end_before_start(self, mock_rental_repo_class, mock_car_repo_class,
                                               mock_car_model):
        """Test registering rental with end date before start raises ValidationError."""
        mock_rental_repo_class.return_value = MagicMock()
        
        mock_car_repo = MagicMock()
        mock_car_model.status = CarStatus.AVAILABLE
        mock_car_repo.get_by_id.return_value = mock_car_model
        mock_car_repo_class.return_value = mock_car_repo
        
        service = RentalService()
        
        with pytest.raises(ValidationError) as exc_info:
            service.register_rental({
                'car_id': '1',
                'customer_name': 'John Doe',
                'start_date': '20240110',
                'end_date': '20240105'
            })
        assert "Start date must be before end date" in str(exc_info.value.message)


class TestRentalServiceEndRental:
    """Tests for RentalService.end_rental method."""
    
    @patch('services.rental_service.CarRepository')
    @patch('services.rental_service.RentalRepository')
    def test_end_rental_success(self, mock_rental_repo_class, mock_car_repo_class,
                                 mock_rental_model, mock_rental_data):
        """Test ending a rental successfully."""
        mock_rental_repo = MagicMock()
        mock_rental_repo.get_by_id.return_value = mock_rental_model
        mock_rental_model.completed = False
        mock_rental_repo.complete_rental.return_value = mock_rental_model
        mock_rental_repo_class.return_value = mock_rental_repo
        
        mock_car_repo = MagicMock()
        mock_car_repo_class.return_value = mock_car_repo
        
        service = RentalService()
        result = service.end_rental(1)
        
        assert result == mock_rental_data
        mock_car_repo.set_available.assert_called_once()
    
    @patch('services.rental_service.CarRepository')
    @patch('services.rental_service.RentalRepository')
    def test_end_rental_not_found(self, mock_rental_repo_class, mock_car_repo_class):
        """Test ending non-existent rental raises NotFoundError."""
        mock_rental_repo = MagicMock()
        mock_rental_repo.get_by_id.return_value = None
        mock_rental_repo_class.return_value = mock_rental_repo
        mock_car_repo_class.return_value = MagicMock()
        
        service = RentalService()
        
        with pytest.raises(NotFoundError) as exc_info:
            service.end_rental(999)
        assert "Rental not found" in str(exc_info.value.message)
    
    @patch('services.rental_service.CarRepository')
    @patch('services.rental_service.RentalRepository')
    def test_end_rental_already_completed(self, mock_rental_repo_class, mock_car_repo_class,
                                           mock_rental_model):
        """Test ending already completed rental raises BusinessLogicError."""
        mock_rental_repo = MagicMock()
        mock_rental_model.completed = True
        mock_rental_repo.get_by_id.return_value = mock_rental_model
        mock_rental_repo_class.return_value = mock_rental_repo
        mock_car_repo_class.return_value = MagicMock()
        
        service = RentalService()
        
        with pytest.raises(BusinessLogicError) as exc_info:
            service.end_rental(1)
        assert "already completed" in str(exc_info.value.message)


class TestRentalServiceDeleteRental:
    """Tests for RentalService.delete_rental method."""
    
    @patch('services.rental_service.CarRepository')
    @patch('services.rental_service.RentalRepository')
    def test_delete_rental_active(self, mock_rental_repo_class, mock_car_repo_class,
                                   mock_rental_model):
        """Test deleting an active rental sets car to available."""
        mock_rental_repo = MagicMock()
        mock_rental_model.completed = False
        mock_rental_model.car_id = 1
        mock_rental_repo.get_by_id.return_value = mock_rental_model
        mock_rental_repo_class.return_value = mock_rental_repo
        
        mock_car_repo = MagicMock()
        mock_car_repo_class.return_value = mock_car_repo
        
        service = RentalService()
        result = service.delete_rental(1)
        
        assert result is True
        mock_car_repo.set_available.assert_called_once_with(1)
        mock_rental_repo.delete_by_id.assert_called_once_with(1)
    
    @patch('services.rental_service.CarRepository')
    @patch('services.rental_service.RentalRepository')
    def test_delete_rental_completed(self, mock_rental_repo_class, mock_car_repo_class,
                                      mock_rental_model):
        """Test deleting completed rental doesn't change car status."""
        mock_rental_repo = MagicMock()
        mock_rental_model.completed = True
        mock_rental_model.car_id = 1
        mock_rental_repo.get_by_id.return_value = mock_rental_model
        mock_rental_repo_class.return_value = mock_rental_repo
        
        mock_car_repo = MagicMock()
        mock_car_repo_class.return_value = mock_car_repo
        
        service = RentalService()
        result = service.delete_rental(1)
        
        assert result is True
        mock_car_repo.set_available.assert_not_called()
        mock_rental_repo.delete_by_id.assert_called_once_with(1)
    
    @patch('services.rental_service.CarRepository')
    @patch('services.rental_service.RentalRepository')
    def test_delete_rental_not_found(self, mock_rental_repo_class, mock_car_repo_class):
        """Test deleting non-existent rental raises NotFoundError."""
        mock_rental_repo = MagicMock()
        mock_rental_repo.get_by_id.return_value = None
        mock_rental_repo_class.return_value = mock_rental_repo
        mock_car_repo_class.return_value = MagicMock()
        
        service = RentalService()
        
        with pytest.raises(NotFoundError) as exc_info:
            service.delete_rental(999)
        assert "Rental not found" in str(exc_info.value.message)


class TestRentalServiceGetActiveRentalByCar:
    """Tests for RentalService.get_active_rental_by_car method."""
    
    @patch('services.rental_service.CarRepository')
    @patch('services.rental_service.RentalRepository')
    def test_get_active_rental_found(self, mock_rental_repo_class, mock_car_repo_class,
                                      mock_rental_model, mock_rental_data):
        """Test getting active rental when one exists."""
        mock_rental_repo = MagicMock()
        mock_rental_repo.get_active_by_car_id.return_value = mock_rental_model
        mock_rental_repo_class.return_value = mock_rental_repo
        mock_car_repo_class.return_value = MagicMock()
        
        service = RentalService()
        result = service.get_active_rental_by_car(1)
        
        assert result == mock_rental_data
    
    @patch('services.rental_service.CarRepository')
    @patch('services.rental_service.RentalRepository')
    def test_get_active_rental_not_found(self, mock_rental_repo_class, mock_car_repo_class):
        """Test getting active rental when none exists returns None."""
        mock_rental_repo = MagicMock()
        mock_rental_repo.get_active_by_car_id.return_value = None
        mock_rental_repo_class.return_value = mock_rental_repo
        mock_car_repo_class.return_value = MagicMock()
        
        service = RentalService()
        result = service.get_active_rental_by_car(1)
        
        assert result is None
