"""Car API routes."""

from flask import Blueprint, jsonify, request
from services import CarService

cars_bp = Blueprint('cars', __name__, url_prefix='/api/cars')
cars_service = CarService()


@cars_bp.route('', methods=['POST'])
def create_car():
    """Create a new car"""
    data = request.get_json()
    car, error = cars_service.create_car(data)
    if error:
        return jsonify({'error': error}), 404
    return jsonify(car.to_dict().id)


@cars_bp.route('/get_cars', methods=['GET'])
def get_cars():
    """Get all cars"""
    cars = cars_service.get_all_cars()
    return jsonify(cars)


@cars_bp.route('/<int:car_id>', methods=['GET'])
def get_car_status(car_id):
    """Get car by ID"""
    car, error = cars_service.get_car(car_id)
    if error:
        return jsonify({'error': error}), 404
    return jsonify(car.status.value)


@cars_bp.route('/<int:car_id>/status', methods=['PUT'])
def update_car_status(car_id):
    """Update car status"""
    data = request.get_json()
    car, error = cars_service.update_car_status(car_id, data)
    if error:
        return jsonify({'error': error}), 404
    return jsonify(car.status.value)


@cars_bp.route('/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    """Delete a car"""
    success, error = cars_service.delete_car(car_id)
    if error:
        return jsonify({'error': error}), 404
    return jsonify({'message': 'Car deleted'})
