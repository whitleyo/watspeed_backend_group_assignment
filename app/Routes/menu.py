from flask import Blueprint, request, jsonify
from injector import inject
from ..Services.menu_service import MenuService
from ..domain.menu_item import MenuItem
from ..mappers.menu_mapper import menu_item_to_response, menu_list_to_response

bp = Blueprint('menu', __name__, url_prefix='/menu')

@inject
@bp.route('/', methods=['GET'])
def get_all_menu_items(menu_service: MenuService):
    """Retrieve all menu items."""
    menu_items = menu_service.get_all_menu_items() # Convert DTOs to dicts
    response = menu_list_to_response(menu_items)
    response_converted = [item.model_dump() for item in response]
    return jsonify(response_converted)  # Convert DTOs to JSON

@inject
@bp.route('/<int:item_id>', methods=['GET'])
def get_menu_item(menu_service: MenuService, item_id: int):
    """Retrieve a specific menu item."""
    menu_item_response = menu_service.get_menu_item(item_id)
    if not menu_item_response:
        return jsonify({'error': 'Menu item not found'}), 404
    response = menu_item_response.model_dump()
    return jsonify(response)  # Convert DTO to JSON

@inject
@bp.route('/', methods=['POST'])
def create_menu_item(menu_service: MenuService):
    """Create a new menu item."""
    data = request.get_json()
    
    if not all(key in data for key in ['name', 'description', 'size', 'price']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    new_item = MenuItem(
        name=data['name'],
        description=data['description'],
        size=data['size'],
        price=data['price']
    )
    
    saved_item = menu_service.add_menu_item(new_item)
    response = menu_item_to_response(saved_item).model_dump()
    return jsonify(response), 201

@inject
@bp.route('/<int:item_id>', methods=['PUT'])
def update_menu_item(menu_service: MenuService, item_id: int):
    """Update an existing menu item."""
    data = request.get_json()
    
    existing_item = menu_service.get_menu_item(item_id)
    if not existing_item:
        return jsonify({'error': 'Menu item not found'}), 404

    updated_item = MenuItem(
        name=data.get('name', existing_item.name),
        description=data.get('description', existing_item.description),
        size=data.get('size', existing_item.size),
        price=data.get('price', existing_item.price)
    )
    
    saved_item = menu_service.update_menu_item(item_id, updated_item)
    response = menu_item_to_response(saved_item).model_dump()
    return jsonify(response)

@inject
@bp.route('/<int:item_id>', methods=['DELETE'])
def delete_menu_item(menu_service: MenuService, item_id: int):
    """Delete a menu item."""
    existing_item = menu_service.get_menu_item(item_id)
    if not existing_item:
        return jsonify({'error': 'Menu item not found'}), 404

    menu_service.remove_menu_item(item_id)
    return jsonify({'message': 'Menu item deleted'}), 200