from flask import Blueprint, request, jsonify
#from app.services.order_service import create_order, modify_order, cancel_order

order_bp = Blueprint('order', __name__, url_prefix='/order')

@order_bp.route('', methods=['POST'])
def order():
    """
    Create a new coffee order.
    ---
    URL: /order
    Method: POST
    Request JSON: {user_id: int, items: [{coffee_type: str, size: str, quantity: int}]}
    Response: {status: 0|1, data: str|dict}
    """
    return jsonify({"status": 0, "data": "data"})

@order_bp.route('/modify/<int:order_id>', methods=['PUT'])
def modify(order_id):
    """
    Update an existing order.
    ---
    URL: /order/modify/<order_id>
    Method: PUT
    Request JSON: {new_items: list, reason: str(optional)}
    Response: {status: 0|1, data: str|dict}
    """
    return jsonify({"status": 0, "data": "data"})

@order_bp.route('/cancel/<int:order_id>', methods=['DELETE'])
def cancel(order_id):
    """
    Cancel an order.
    ---
    URL: /order/cancel/<order_id>
    Method: DELETE
    Response: {status: 0|1, data: str|dict}
    """
    return jsonify({"status": 0, "data": "data"})