"""Rentals API routes."""

from flask import Blueprint, jsonify, request
from services import RentalService

rentals_bp = Blueprint('rentals', __name__, url_prefix='/api/rentals')
rentals_service = RentalService()


@rentals_bp.route('/register', methods=['POST'])
def register_rental():
    """Register a new rental"""
    data = request.get_json()
    rental, error = rentals_service.register_rental(data)
    if error:
        return jsonify({'error': error}), 400
    return jsonify(rental), 201


@rentals_bp.route('/get_rentals', methods=['GET'])
def get_rentals():
    """Get all rentals"""
    rentals = rentals_service.get_all_rentals()
    return jsonify(rentals)


@rentals_bp.route('/<int:rental_id>', methods=['GET'])
def get_rental(rental_id):
    """Get rental by ID"""
    rental, error = rentals_service.get_rental(rental_id)
    if error:
        return jsonify({'error': error}), 404
    return jsonify(rental.to_dict())


@rentals_bp.route('/<int:rental_id>/end', methods=['PUT'])
def end_rental(rental_id):
    """End/complete a rental"""
    rental, error = rentals_service.end_rental(rental_id)
    if error:
        return jsonify({'error': error}), 400
    return jsonify(rental)


@rentals_bp.route('/<int:rental_id>', methods=['DELETE'])
def delete_rental(rental_id):
    """Delete a rental"""
    success, error = rentals_service.delete_rental(rental_id)
    if error:
        return jsonify({'error': error}), 404
    return jsonify({'message': 'Rental deleted'})
