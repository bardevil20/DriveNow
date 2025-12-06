"""Car API routes."""

import logging
from flask import Blueprint, jsonify, request
from services import CarService
from core.exceptions import AppException

cars_bp = Blueprint('cars', __name__, url_prefix='/api/cars')
cars_service = CarService()
logger = logging.getLogger(__name__)


@cars_bp.route('', methods=['POST'])
def create_car():
    """Create a new car"""
    data = request.get_json()
    if not data:
        logger.warning("Create car failed: No data provided")
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        car = cars_service.create_car(data)
        logger.info(f"Car created successfully: {car['id']}")
        return jsonify(car), 201
    except AppException as e:
        logger.error(f"Create car failed: {e.message}")
        return jsonify({'error': e.message}), e.status_code


@cars_bp.route('/get_cars', methods=['GET'])
def get_cars():
    """Get all cars"""
    try:
        cars = cars_service.get_all_cars()
        logger.info(f"Fetched {len(cars)} cars")
        return jsonify(cars), 200
    except AppException as e:
        logger.error(f"Get cars failed: {e.message}")
        return jsonify({'error': e.message}), e.status_code


@cars_bp.route('/<int:car_id>', methods=['GET'])
def get_car(car_id):
    """Get car by ID"""
    try:
        car = cars_service.get_car(car_id)
        logger.info(f"Fetched car: {car_id}")
        return jsonify(car), 200
    except AppException as e:
        logger.error(f"Get car {car_id} failed: {e.message}")
        return jsonify({'error': e.message}), e.status_code


@cars_bp.route('/<int:car_id>/status', methods=['PUT'])
def update_car_status(car_id):
    """Update car status"""
    data = request.get_json()
    if not data or 'status' not in data:
        logger.warning(f"Update car status {car_id} failed: Status is required")
        return jsonify({'error': 'Status is required'}), 400
    
    try:
        car = cars_service.update_car_status(car_id, data['status'])
        logger.info(f"Car {car_id} status updated to {car['status']}")
        return jsonify(car), 200
    except AppException as e:
        logger.error(f"Update car status {car_id} failed: {e.message}")
        return jsonify({'error': e.message}), e.status_code


@cars_bp.route('/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    """Delete a car (completes active rental if car is in use)"""
    try:
        cars_service.delete_car(car_id)
        logger.info(f"Car deleted: {car_id}")
        return jsonify({'message': 'Car deleted'}), 200
    except AppException as e:
        logger.error(f"Delete car {car_id} failed: {e.message}")
        return jsonify({'error': e.message}), e.status_code
