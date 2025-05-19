import pytest
from flask import Flask, json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.domain.order import Base, Order, OrderItem
from app.domain.menu_item import MenuItem
from app.Services.order_service import OrderService
from app.daos.order_dao import OrderDAO
from app.Routes.orders import bp

# Test database setup
TEST_DB_URL = "postgresql://test_user:test_password@localhost/test_db"
engine = create_engine(TEST_DB_URL)
Session = sessionmaker(bind=engine)

@pytest.fixture(scope="session")
def setup_database():
    """Ensures a fresh test database before running tests."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def db_session(setup_database):
    """Provides a fresh database session for each test."""
    session = Session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def order_dao(db_session):
    """Provides an OrderDAO instance for actual DB interaction."""
    return OrderDAO(db_session)

@pytest.fixture
def order_service(order_dao):
    """Provides an OrderService instance with real DB interaction."""
    return OrderService(order_dao)

@pytest.fixture(scope="function")
def client(order_service):
    """Sets up Flask test client with Flask-Injector integration."""
    from injector import Binder, Injector, singleton
    from flask_injector import FlaskInjector
    from app import create_app
    app = create_app()
    app.testing = True

    def configure(binder: Binder):
        binder.bind(OrderService, to=order_service, scope=singleton)

    injector = Injector([configure])
    FlaskInjector(app=app, injector=injector)

    # app.register_blueprint(bp)  # ✅ Routes should only be registered AFTER injection setup

    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_menu_items(db_session):
    """Creates and stores multiple sample menu items."""
    items = [
        MenuItem(name="Espresso", description="Bold coffee", size="Medium", price=3.0),
        MenuItem(name="Cappuccino", description="Smooth coffee blend", size="Large", price=4.0)
    ]
    db_session.add_all(items)
    db_session.commit()
    [db_session.refresh(item) for item in items]
    return items

@pytest.fixture(autouse=True)
def clean_orders(db_session):
    """Ensures test database starts fresh before each test."""
    db_session.query(Order).delete()
    db_session.query(OrderItem).delete()
    db_session.commit()

def create_order(client, customer_name: str, menu_items: list) -> dict:
    """Helper function to create an order via API."""
    response = client.post('/order', json={
        "customer_name": customer_name,
        "items": [{"menu_item_id": item.id, "quantity": 2} for item in menu_items]
    })
    print('debug response')
    print(response.get_json())
    return response.get_json()

# ---- Order API Tests ----

def test_create_order(client, sample_menu_items):
    """Test creating a new order via POST /order."""
    print(client.application.url_map)
    data = create_order(client, "Alice", sample_menu_items)
    assert data["status"] == "pending"
    assert data["message"] == "Order saved successfully"

def test_modify_order_success(client, sample_menu_items):
    """Test modifying an existing order via PUT /order/modify."""
    created_order = create_order(client, "Bob", sample_menu_items)
    order_id = created_order["order_id"]

    modify_response = client.put('/order/modify', json={
        "order_id": order_id,
        "items": [{"menu_item_id": item.id, "quantity": 4} for item in sample_menu_items]
    })
    data = modify_response.get_json()

    assert modify_response.status_code == 200
    assert data["status"] == "pending"
    assert data["message"] == "Order modified successfully"

def test_modify_order_not_found(client):
    """Test modifying a non-existent order."""
    modify_response = client.put('/order/modify', json={
        "order_id": 999,
        "items": [{"menu_item_id": 1, "quantity": 1}]
    })
    data = modify_response.get_json()

    assert modify_response.status_code == 404
    assert data["status"] == 1
    assert data["message"] == "Order not found"

def test_cancel_order_success(client, sample_menu_items):
    """Test canceling an existing order via DELETE /order/cancel/{order_id}."""
    created_order = create_order(client, "Charlie", sample_menu_items)
    order_id = created_order["order_id"]

    cancel_response = client.delete(f'/order/cancel/{order_id}')
    data = cancel_response.get_json()

    assert cancel_response.status_code == 200
    assert data["status"] == 0
    assert data["message"] == "Order deleted successfully"

def test_cancel_order_not_found(client):
    """Test canceling a non-existent order."""
    cancel_response = client.delete('/order/cancel/999')
    data = cancel_response.get_json()

    assert cancel_response.status_code == 404
    assert data["status"] == 1
    assert data["message"] == "Order not found"

def test_get_order_success(client, sample_menu_items):
    """Test fetching an existing order via GET /order/{order_id}."""
    created_order = create_order(client, "David", sample_menu_items)
    order_id = created_order["order_id"]

    get_response = client.get(f'/order/{order_id}')
    data = get_response.get_json()

    assert get_response.status_code == 200
    assert data["customer_name"] == "David"
    assert len(data["order_items"]) == len(sample_menu_items)
    assert data["status"] == "pending"

def test_get_order_not_found(client):
    """Test fetching a non-existent order."""
    get_response = client.get('/order/999')
    data = get_response.get_json()

    assert get_response.status_code == 404
    assert data["status"] == 1
    assert data["message"] == "Order not found"

def test_get_all_orders(client, sample_menu_items):
    """Test fetching all orders via GET /order/all."""
    create_order(client, "Eve", sample_menu_items)
    create_order(client, "Frank", sample_menu_items)

    get_response = client.get('/order/all')
    data = get_response.get_json()

    assert get_response.status_code == 200
    assert len(data) == 2
    assert data[0]["customer_name"] == "Eve"
    assert data[1]["customer_name"] == "Frank"