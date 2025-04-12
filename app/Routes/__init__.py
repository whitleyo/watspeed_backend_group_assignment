from flask import Blueprint
from .auth import auth_bp
from .menu import menu_bp
from .orders import orders_bp

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

def register_blueprints(app):
    app.register_blueprint(api_v1)
    api_v1.register_blueprint(auth_bp)
    api_v1.register_blueprint(menu_bp)
    api_v1.register_blueprint(orders_bp) 
