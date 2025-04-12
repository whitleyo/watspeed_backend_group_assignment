from flask import Blueprint, request, jsonify

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')