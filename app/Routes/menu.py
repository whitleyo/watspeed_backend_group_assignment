from flask import Blueprint, request, jsonify

menu_bp = Blueprint('menu', __name__, url_prefix='/menu')

# Menu items. Can be replaced with requests to SQL database in future.
# menu_items = [
#     {"id": 1, "name": "Espresso", "price": 3.00},
#     {"id": 2, "name": "Latte", "price": 4.50},
#     {"id": 3, "name": "Cappuccino", "price": 4.00}
# ]

@menu_bp.route('/', methods=['GET'])
def get_menu():
    """Retrieve the coffee menu."""
    # return jsonify(menu_items), 200
    # For now, we return a status code and a placeholder string
    # in json format.
    status=int(0)
    data=str("data")
    return jsonify({'status': status, 'data': data})