from flask import Blueprint, jsonify

reservations_bp = Blueprint('reservations', __name__, url_prefix='/reservations')