"""Rentals API routes."""

import logging
from flask import Blueprint, jsonify, request
from services import RentalService
from core.exceptions import AppException

rentals_bp = Blueprint('rentals', __name__, url_prefix='/api/rentals')
rentals_service = RentalService()
logger = logging.getLogger(__name__)


@rentals_bp.route('/register', methods=['POST'])
def register_rental():
    """Register a new rental"""
    data = request.get_json()
    if not data:
        logger.warning("Register rental failed: No data provided")
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        rental = rentals_service.register_rental(data)
        logger.info(f"Rental registered successfully: {rental['rental_id']}")
        return jsonify(rental), 201
    except AppException as e:
        logger.error(f"Register rental failed: {e.message}")
        return jsonify({'error': e.message}), e.status_code


@rentals_bp.route('/get_rentals', methods=['GET'])
def get_rentals():
    """Get all rentals"""
    try:
        rentals = rentals_service.get_all_rentals()
        logger.info(f"Fetched {len(rentals)} rentals")
        return jsonify(rentals), 200
    except AppException as e:
        logger.error(f"Get rentals failed: {e.message}")
        return jsonify({'error': e.message}), e.status_code


@rentals_bp.route('/<int:rental_id>', methods=['GET'])
def get_rental(rental_id):
    """Get rental by ID"""
    try:
        rental = rentals_service.get_rental(rental_id)
        logger.info(f"Fetched rental: {rental_id}")
        return jsonify(rental), 200
    except AppException as e:
        logger.error(f"Get rental {rental_id} failed: {e.message}")
        return jsonify({'error': e.message}), e.status_code


@rentals_bp.route('/<int:rental_id>/end', methods=['PUT'])
def end_rental(rental_id):
    """End/complete a rental"""
    try:
        rental = rentals_service.end_rental(rental_id)
        logger.info(f"Rental completed: {rental_id}")
        return jsonify(rental), 200
    except AppException as e:
        logger.error(f"End rental {rental_id} failed: {e.message}")
        return jsonify({'error': e.message}), e.status_code


@rentals_bp.route('/<int:rental_id>', methods=['DELETE'])
def delete_rental(rental_id):
    """Delete a rental (sets car to AVAILABLE if rental was active)"""
    try:
        rentals_service.delete_rental(rental_id)
        logger.info(f"Rental deleted: {rental_id}")
        return jsonify({'message': 'Rental deleted'}), 200
    except AppException as e:
        logger.error(f"Delete rental {rental_id} failed: {e.message}")
        return jsonify({'error': e.message}), e.status_code
