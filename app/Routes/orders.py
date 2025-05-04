from flask import Blueprint, request, jsonify
#from app.services.order_service import create_order, modify_order, cancel_order

order_bp = Blueprint('order', __name__, url_prefix='/order')

@order_bp.route('', methods=['POST'])
def order():
    """Create new order"""
    data = request.get_json()

    if not data or "customer_id" not in data or "items" not in data or "total_price" not in data:
        return jsonify({"error": "Missing required fields"}), 400  # Validate input data

    new_order = {
        "order_id": 123,  # Mock ID for now
        "customer_id": data["customer_id"],
        "items": data["items"],
        "total_price": data["total_price"]
    }

    return jsonify({"status": 0, "data": new_order}), 201  # Explicitly return 201

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
    """Cancel order"""
    
    # Mock database check (replace with actual lookup logic)
    existing_orders = [1, 2, 3]  # Sample order IDs
    
    if order_id not in existing_orders:
        return jsonify({"error": "Order not found"}), 404  # Return 404 if order doesn't exist

    return jsonify({"status": 0, "data": f"Order {order_id} canceled"}), 200