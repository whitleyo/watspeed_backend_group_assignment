from flask import Flask
from flask_injector import FlaskInjector
from flask_socketio import SocketIO
from injector import Binder
from .config import Config
from .Routes.reservation import bp as reservations_bp
from .Routes.table import bp as tables_bp
from .Routes.menu import bp as menu_bp
from .Routes.orders import bp as order_bp
from .Routes.images import bp as images_bp
from .Routes.calculator import bp as calculator_bp
from .Services.reservation_service import ReservationService
from .Services.table_service import TableService
from .Services.menu_service import MenuService
from .Services.order_service import OrderService
from .daos.reservation_dao import ReservationDAO
from .daos.table_dao import TableDAO
from .daos.menu_dao import MenuDAO
from .daos.order_dao import OrderDAO

# Initialize SocketIO at module level
socketio = SocketIO(async_mode='threading')

# Dependency injection configuration
def configure(binder: Binder):
    """Configure dependency injection bindings"""
    # DAO bindings
    binder.bind(ReservationDAO, to=ReservationDAO())
    binder.bind(TableDAO, to=TableDAO())
    binder.bind(MenuDAO, to=MenuDAO())
    binder.bind(OrderDAO, to=OrderDAO())
    
    # Service layer bindings
    binder.bind(ReservationService, to=ReservationService(
        reservation_dao=binder.injector.get(ReservationDAO),
        table_dao=binder.injector.get(TableDAO)
    ))
    binder.bind(TableService, to=TableService(
        table_dao=binder.injector.get(TableDAO)
    ))
    binder.bind(MenuService, to=MenuService(
        menu_dao=binder.injector.get(MenuDAO)
    ))
    binder.bind(OrderService, to=OrderService(
        order_dao=binder.injector.get(OrderDAO)
    ))

def create_app():
    """Application factory function"""
    app = Flask(__name__)
    
    # Configure application settings
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(reservations_bp)
    app.register_blueprint(tables_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(images_bp)
    app.register_blueprint(calculator_bp)
    
    # Initialize SocketIO
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Configure dependency injection
    FlaskInjector(app=app, modules=[configure])
    
    # Register WebSocket handlers with app context
    with app.app_context():
        from .websocket_handler import register_socketio_handlers
        register_socketio_handlers(socketio, app)
    
    return app