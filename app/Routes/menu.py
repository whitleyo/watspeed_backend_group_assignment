from flask import Blueprint, request, jsonify
from injector import inject
from ..Services.menu_service import MenuService
from ..domain.menu_item import MenuItem

bp = Blueprint('menu', __name__, url_prefix='/menu')

@inject
@bp.route('/', methods=['GET'])
def get_all_menu_items(menu_service: MenuService):
    """Retrieve all menu items."""
    menu_items = menu_service.get_all_menu_items()
    return jsonify([item.dict() for item in menu_items])  # Convert DTOs to JSON

@inject
@bp.route('/<int:item_id>', methods=['GET'])
def get_menu_item(menu_service: MenuService, item_id: int):
    """Retrieve a specific menu item."""
    menu_item = menu_service.get_menu_item(item_id)
    
    if not menu_item:
        return jsonify({'error': 'Menu item not found'}), 404
    
    return jsonify(menu_item.dict())  # Convert DTO to JSON

@inject
@bp.route('/', methods=['POST'])
def create_menu_item(menu_service: MenuService):
    """Create a new menu item."""
    data = request.get_json()
    
    if not all(key in data for key in ['name', 'description', 'sizes', 'prices']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    new_item = MenuItem(
        id=0,  # ID 0 ensures a new item is created
        name=data['name'],
        description=data['description'],
        sizes=data['sizes'],
        prices=data['prices']
    )
    
    saved_item = menu_service.add_or_update_menu_item(0, new_item)
    return jsonify(saved_item.dict()), 201

@inject
@bp.route('/<int:item_id>', methods=['PUT'])
def update_menu_item(menu_service: MenuService, item_id: int):
    """Update an existing menu item."""
    data = request.get_json()
    
    existing_item = menu_service.get_menu_item(item_id)
    if not existing_item:
        return jsonify({'error': 'Menu item not found'}), 404

    updated_item = MenuItem(
        id=item_id,
        name=data.get('name', existing_item.name),
        description=data.get('description', existing_item.description),
        sizes=data.get('sizes', existing_item.sizes),
        prices=data.get('prices', existing_item.prices)
    )
    
    saved_item = menu_service.add_or_update_menu_item(item_id, updated_item)
    return jsonify(saved_item.dict())

@inject
@bp.route('/<int:item_id>', methods=['DELETE'])
def delete_menu_item(menu_service: MenuService, item_id: int):
    """Delete a menu item."""
    existing_item = menu_service.get_menu_item(item_id)
    if not existing_item:
        return jsonify({'error': 'Menu item not found'}), 404

    menu_service.remove_menu_item(item_id)
    return jsonify({'message': 'Menu item deleted'}), 200