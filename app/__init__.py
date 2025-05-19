from flask import Flask
from flask_injector import FlaskInjector
from injector import Binder
#from .config import Config
from .Routes.reservation import bp as reservations_bp
from .Routes.table import bp as tables_bp
from .Routes.menu import bp as menu_bp
from .Routes.orders import bp as order_bp
from .Services.reservation_service import ReservationService
from .Services.table_service import TableService
from .Services.menu_service import MenuService
from .Services.order_service import OrderService
from .daos.reservation_dao import ReservationDAO
from .daos.table_dao import TableDAO
from .daos.menu_dao import MenuDAO
from .daos.order_dao import OrderDAO

def configure(binder: Binder):
    """Configure dependency injection bindings"""
    binder.bind(ReservationDAO, to=ReservationDAO())
    binder.bind(TableDAO, to=TableDAO())
    binder.bind(MenuDAO, to=MenuDAO())
    binder.bind(OrderDAO, to=OrderDAO())
    binder.bind(ReservationService, to=ReservationService(
        reservation_dao=ReservationDAO(),
        table_dao=TableDAO()
    ))
    binder.bind(TableService, to=TableService(
        table_dao=TableDAO()
    ))
    binder.bind(MenuService, to=MenuService(
        menu_dao=MenuDAO()
    ))
    binder.bind(OrderService, to=OrderService(
        order_dao=OrderDAO()
    ))

def create_app():
    app = Flask(__name__)
    #app.config.from_object(config_class)
    
    # Register blueprints
    app.register_blueprint(reservations_bp)
    app.register_blueprint(tables_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(order_bp)
    #app.register_blueprint(auth_bp)
    #app.register_blueprint(api_v1) 
    # Configure dependency injection
    FlaskInjector(app=app, modules=[configure])
    
    return app