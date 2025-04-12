from flask import Blueprint, request, jsonify

menu_bp = Blueprint('menu', __name__, url_prefix='/menu')