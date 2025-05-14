from flask import Blueprint, request, jsonify
from injector import inject
from ..Services.reservation_service import ReservationService
from ..domain.reservation import Reservation

bp = Blueprint('reservations', __name__, url_prefix='/reservations')

@inject
@bp.route('/', methods=['POST'])
def create_reservation(reservation_service: ReservationService):
    """Create a new reservation"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['table_id', 'customer_name', 'people_count', 'time']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Create reservation
    reservation = reservation_service.create_reservation(
        table_id=data['table_id'],
        customer_name=data['customer_name'],
        people_count=data['people_count'],
        time=data['time']
    )
    
    if not reservation:
        return jsonify({'error': 'Could not create reservation'}), 400
    
    return jsonify({
        'reservation_id': reservation.id,
        'table_id': reservation.table_id,
        'customer_name': reservation.customer_name,
        'people_count': reservation.people_count,
        'time': reservation.time
    }), 201

@inject
@bp.route('/<int:reservation_id>', methods=['GET'])
def get_reservation(reservation_service: ReservationService, reservation_id: int):
    """Get a specific reservation"""
    reservation = reservation_service.get_reservation(reservation_id)
    
    if not reservation:
        return jsonify({'error': 'Reservation not found'}), 404
    
    return jsonify({
        'reservation_id': reservation.id,
        'table_id': reservation.table_id,
        'customer_name': reservation.customer_name,
        'people_count': reservation.people_count,
        'time': reservation.time
    })

@inject
@bp.route('/customer/<string:customer_name>', methods=['GET'])
def get_customer_reservations(reservation_service: ReservationService, customer_name: str):
    """Get all reservations for a customer"""
    reservations = reservation_service.get_customer_reservations(customer_name)
    return jsonify([{
        'reservation_id': r.reservation_id,
        'table_id': r.table_id,
        'people_count': r.people_count,
        'time': r.time
    } for r in reservations])

@inject
@bp.route('/<int:reservation_id>', methods=['PUT'])
def update_reservation(reservation_service: ReservationService, reservation_id: int):
    """Update a reservation"""
    data = request.get_json()
    
    # Validate at least one updatable field is present
    updatable_fields = ['table_id', 'customer_name', 'people_count', 'time']
    if not any(field in data for field in updatable_fields):
        return jsonify({'error': 'No valid fields to update'}), 400
    
    # Perform update
    updated_reservation = reservation_service.update_reservation(
        reservation_id=reservation_id,
        **data
    )
    
    if not updated_reservation:
        return jsonify({'error': 'Could not update reservation'}), 400
    
    return jsonify({
        'reservation_id': updated_reservation.id,
        'table_id': updated_reservation.table_id,
        'customer_name': updated_reservation.customer_name,
        'people_count': updated_reservation.people_count,
        'time': updated_reservation.time
    })

@inject
@bp.route('/<int:reservation_id>', methods=['DELETE'])
def cancel_reservation(reservation_service: ReservationService, reservation_id: int):
    """Cancel a reservation"""
    success = reservation_service.cancel_reservation(reservation_id)
    
    if not success:
        return jsonify({'error': 'Reservation not found'}), 404
    
    return jsonify({'message': 'Reservation canceled'}), 200

@inject
@bp.route('/availability', methods=['GET'])
def get_availability(reservation_service: ReservationService):
    """Get available tables for a time and party size"""
    time = request.args.get('time')
    people_count = request.args.get('people_count', type=int)
    
    if not time or not people_count:
        return jsonify({'error': 'Missing time or people_count parameters'}), 400
    
    available_tables = reservation_service.get_available_tables(time, people_count)
    return jsonify(available_tables)