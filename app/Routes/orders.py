from flask import Blueprint, request, jsonify
from injector import inject
from app.Services.order_service import OrderService
from app.daos.order_dao import OrderDAO
from app.messages.requests.order_request_dto import OrderRequestDTO, ModifyOrderRequestDTO, DeleteOrderRequestDTO

bp = Blueprint('order', __name__, url_prefix='/order')

@inject
@bp.route('', methods=['POST'])
def create_order(order_service: OrderService):
    """Create a new order."""
    data = request.get_json()
    try:
        order_dto = OrderRequestDTO(**data)
        response_dto = order_service.save_order(order_dto)
        if response_dto:
            return jsonify(response_dto.dict()), 201
        else:
            return jsonify({"status": 1, "message": "Order could not be created"}), 400
    except ValueError as e:
        return jsonify({"status": 1, "message": str(e)}), 400

@inject
@bp.route('/modify', methods=['PUT'])
def modify_order(order_service: OrderService):
    """Update an existing order."""
    data = request.get_json()
    try:
        modify_dto = ModifyOrderRequestDTO(**data)
        response_dto = order_service.modify_order(modify_dto)
        if response_dto:
            return jsonify(response_dto.dict()), 200
        else:
           return jsonify({"status": 1, "message": "Order not found"}), 404
    except ValueError as e:
        return jsonify({"status": 1, "message": str(e)}), 400

@inject
@bp.route('/cancel/<int:order_id>', methods=['DELETE'])
def cancel_order(order_id, order_service: OrderService):
    """Cancel an order."""
    delete_request = DeleteOrderRequestDTO(order_id=order_id)
    delete_response = order_service.delete_order(delete_request)

    if delete_response.status == 0:
        return jsonify(delete_response.dict()), 200
    elif delete_response.status == 1:
        return jsonify({"status": 1, "message": "Order not found"}), 404
    else:
        return jsonify({"status": 2, "message": "Unexpected error"}), 500

@inject
@bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id, order_service: OrderService):
    """Get an order by ID."""
    order = order_service.find_order(order_id)
    if order:
        return jsonify(order.dict()), 200
    return jsonify({"status": 1, "message": "Order not found"}), 404

@inject
@bp.route('/all', methods=['GET'])
def get_all_orders(order_service: OrderService):
    """Get all orders."""
    orders = order_service.find_all_orders()
    return jsonify([order.dict() for order in orders]), 200
