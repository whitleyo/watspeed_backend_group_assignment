from flask import Blueprint, request, jsonify
#from app.services.order_service import create_order, modify_order, cancel_order

order_bp = Blueprint('order', __name__, url_prefix='/order')

@order_bp.route('', methods=['POST'])
def order():
    """
    Create new order
    Returns:
        JSON response with status (int) and data (str) fields.
    """
    data = request.get_json()
    #result = create_order(data)
    return jsonify({ "status": 0, "data": "data" })

@order_bp.route('/modify/<int:order_id>', methods=['PUT'])
def modify(order_id):
    """
    Update existing order
    Args:
        order_id (int): The ID of the order to modify.
    Returns:
        JSON response with status (int) and data (str) fields.
    """
    data = request.get_json()
    #result = modify_order(order_id, data)
    return jsonify({ "status": 0, "data": "data" })

@order_bp.route('/cancel/<int:order_id>', methods=['DELETE'])
def cancel(order_id):
    """
    Cancel order
    Args:
        order_id (int): The ID of the order to cancel.
    Returns:
        JSON response with status (int) and data (str) fields.
    """
    #result = cancel_order(order_id)
    return jsonify({ "status": 0, "data": "data" })