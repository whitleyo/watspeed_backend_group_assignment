from flask import Flask
from flask_injector import FlaskInjector
from injector import Binder
#from .config import Config
from .Routes.reservation import bp as reservations_bp
from .Routes.table import bp as tables_bp
from .Services.reservation_service import ReservationService
from .Services.table_service import TableService
from .daos.reservation_dao import ReservationDAO
from .daos.table_dao import TableDAO

def configure(binder: Binder):
    """Configure dependency injection bindings"""
    binder.bind(ReservationDAO, to=ReservationDAO())
    binder.bind(TableDAO, to=TableDAO())
    binder.bind(ReservationService, to=ReservationService(
        reservation_dao=ReservationDAO(),
        table_dao=TableDAO()
    ))
    binder.bind(TableService, to=TableService(
        table_dao=TableDAO()
    ))

def create_app():
    app = Flask(__name__)
    #app.config.from_object(config_class)
    
    # Register blueprints
    app.register_blueprint(reservations_bp)
    app.register_blueprint(tables_bp)
    
    # Configure dependency injection
    FlaskInjector(app=app, modules=[configure])
    
    return app