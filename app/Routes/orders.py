from flask import Blueprint, request, jsonify
from app.Services.order_service import OrderService
from app.daos.order_dao import OrderDAO
from app.messages.requests.order_request_dto import OrderRequestDTO, ModifyOrderRequestDTO, DeleteOrderRequestDTO

order_bp = Blueprint('order', __name__, url_prefix='/order')

dao = OrderDAO()
order_service = OrderService(dao)

@order_bp.route('', methods=['POST'])
def order():
    """Create new order"""
    data = request.get_json()
    order_dto = OrderRequestDTO(**data)
    response_dto = order_service.save_order(order_dto)
    return jsonify(response_dto.__dict__)

@order_bp.route('/modify', methods=['PUT'])
def modify():
    """
    Update existing order
    Returns:
        JSON response with status (int) and data (str) fields.
    """
    data = request.get_json()
    modify_dto = ModifyOrderRequestDTO(**data)
    response_dto = order_service.modify_order(modify_dto)

    if response_dto:
        return jsonify(response_dto.__dict__)
    return jsonify({"status": 1, "message": "Order not found"}), 404

@order_bp.route('/cancel/<int:order_id>', methods=['DELETE'])
def cancel(order_id):
    """
    Cancel order
    Returns:
        JSON response with status (int) and data (str) fields.
    """
    delete_request = DeleteOrderRequestDTO(order_id=order_id)
    delete_response = order_service.delete_order(delete_request)
    if delete_response.status == 0:
        return jsonify(delete_response.__dict__), 200
    elif delete_response.status == 1:
        # If the order was not found, return a 404 error
        # with a message indicating that the order was not found.
        return jsonify({"status": 1, "message": "Order not found"}), 404
    else:
        return jsonify(delete_response.__dict__), 500
