from flask import Blueprint, jsonify

reservations_bp = Blueprint('reservations', __name__, url_prefix='/reservations')

# Temporary storage for reservations (Replace with database later)
reserved_seats = set()

@reservations_bp.route('/reserve-seat/<int:seat_id>', methods=['POST'])
def reserve_seat(seat_id):
    """
    Reserve a seat by seat_id.
    
    Args:
        seat_id (int): integer seat id
    Returns:
        json with {'data': str, 'status': int}
    """
    # placeholder for purposes of assignment
    data = 'data'
    if seat_id in reserved_seats:
        # return jsonify({"error": "Seat not available"}), 404  # Seat already reserved
        status = 1
    else:
        status = 0
        reserved_seats.add(seat_id)  # Reserve the seat
    # return jsonify({"message": "Seat reserved successfully", "seat_id": seat_id}), 201
    return jsonify({"data": data, "status": status})

@reservations_bp.route('/cancel-seat/<int:seat_id>', methods=['DELETE'])
def cancel_reservation(seat_id):
    """
    Cancel a seat reservation by seat_id.
    
    Args:
        seat_id (int): integer seat id
    Returns:
        json with {'data': str, 'status': int}
    """
    # placeholder for purposes of assignment
    data = 'data'
    if seat_id not in reserved_seats:
        # return jsonify({"error": "Reservation not found"}), 404  # Seat was never reserved
        status = 1
    else:
        status = 0
        reserved_seats.remove(seat_id)  # Cancel the reservation
    # return jsonify({"message": "Reservation canceled successfully", "seat_id": seat_id}), 200
    return jsonify({"data": data, "status": status})