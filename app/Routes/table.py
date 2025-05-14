from flask import Blueprint, jsonify
from injector import inject
from ..Services.table_service import TableService

bp = Blueprint('tables', __name__, url_prefix='/tables')

@inject
@bp.route('/', methods=['GET'])
def get_all_tables(table_service: TableService):
    """Get all tables"""
    tables = table_service.get_all_tables()
    return jsonify([{
        'id': t.id,
        'location': t.location,
        'capacity': t.capacity
    } for t in tables])

@inject
@bp.route('/<int:table_id>', methods=['GET'])
def get_table(table_service: TableService, table_id: int):
    """Get a specific table"""
    table = table_service.get_table(table_id)
    
    if not table:
        return jsonify({'error': 'Table not found'}), 404
    
    return jsonify({
        'id': table.id,
        'location': table.location,
        'capacity': table.capacity
    })

@inject
@bp.route('/shop/<shop_location>', methods=['GET'])
def get_shop_tables(table_service: TableService, shop_location: str):
    """Get all tables in a specific shop"""
    tables = table_service.get_tables_by_location(shop_location)
    return jsonify([{
        'id': t.id,
        'capacity': t.capacity
    } for t in tables])