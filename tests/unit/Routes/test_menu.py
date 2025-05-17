import pytest
from flask import Flask, json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.domain.menu_item import Base, MenuItem
from app.Services.menu_service import MenuService
from app.daos.menu_dao import MenuDAO
from app.Routes.menu import bp  # Import the menu routes

# Test database setup
TEST_DB_URL = "postgresql://test_user:test_password@localhost/test_db"
engine = create_engine(TEST_DB_URL)
Session = sessionmaker(bind=engine)

@pytest.fixture(scope="session")
def setup_database():
    """Ensures a fresh test database before running tests."""
    Base.metadata.create_all(engine)  # Create tables
    yield
    Base.metadata.drop_all(engine)  # Cleanup after tests

@pytest.fixture(scope="function")
def db_session(setup_database):
    """Provides a fresh database session for each test."""
    session = Session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def menu_dao(db_session):
    """Provides a MenuDAO instance for actual DB interaction."""
    return MenuDAO(db_session)

@pytest.fixture
def menu_service(menu_dao):
    """Provides a MenuService instance with real DB interaction."""
    return MenuService(menu_dao)

@pytest.fixture(scope="function")
def client(menu_service):
    """Sets up Flask test client with correct Flask-Injector integration."""
    from injector import Binder, Injector, singleton
    from flask_injector import FlaskInjector
    app = Flask(__name__)
    app.testing = True
    # Ensure Flask-Injector binds MenuService before request handling
    def configure(binder: Binder):
        binder.bind(MenuService, to=menu_service, scope=singleton)
    injector = Injector([configure])
    FlaskInjector(app=app, injector=injector)  # ✅ Attach Injector before registering blueprints
    app.register_blueprint(bp)  # ✅ Register routes after dependency injection setup
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_menu_item(db_session):
    """Creates a real menu item in the database."""
    item = MenuItem(
        name="Cappuccino",
        description="Frothy and smooth coffee",
        size="Medium",
        price=4.0
    )
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    return item

@pytest.fixture
def sample_menu_item2(db_session):
    """Creates a real menu item in the database."""
    item = MenuItem(
        name="Iced Latte",
        description="Chilled coffee with milk",
        size="Large",
        price=2.0
    )
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    return item

@pytest.fixture(autouse=True)
def clean_menu_items(db_session):
    """Ensure test database starts fresh before each test."""
    db_session.query(MenuItem).delete()
    db_session.commit()

# ---- Retrieval Tests ----
def test_get_all_menu_items_success(client, sample_menu_item, sample_menu_item2):
    """Test retrieving all menu items."""
    res = client.get('/menu/')
    assert res.status_code == 200
    assert len(res.json) == 2
    assert res.json[0]["name"] == "Cappuccino"
    assert res.json[1]["price"] == 2.0


def test_get_menu_item_success(client, sample_menu_item):
    """Test retrieving a specific menu item."""
    res = client.get(f'/menu/{sample_menu_item.id}')
    assert res.status_code == 200
    assert res.json["name"] == "Cappuccino"

def test_get_menu_item_not_found(client):
    """Test retrieving a non-existent menu item."""
    res = client.get('/menu/999')
    assert res.status_code == 404
    assert res.json == {"error": "Menu item not found"}

# ---- Creation & Updating Tests ----
def test_create_menu_item_success(client):
    """Test creating a new menu item."""
    data = {
        "name": "Latte",
        "description": "Milk coffee",
        "size": "Medium",
        "price": 4.2
    }
    res = client.post('/menu/', json=data)

    assert res.status_code == 201
    assert res.json["name"] == "Latte"

def test_update_menu_item_success(client, sample_menu_item):
    """Test updating an existing menu item."""
    data = {"name": "Updated Cappuccino", "description": "Stronger coffee"}
    res = client.put(f'/menu/{sample_menu_item.id}', json=data)

    assert res.status_code == 200
    assert res.json["name"] == "Updated Cappuccino"

# ---- Deletion Tests ----
def test_delete_menu_item_success(client, sample_menu_item):
    """Test deleting a menu item."""
    res = client.delete(f'/menu/{sample_menu_item.id}')

    assert res.status_code == 200
    assert res.json == {"message": "Menu item deleted"}

def test_delete_menu_item_not_found(client):
    """Test deleting a non-existent menu item."""
    res = client.delete('/menu/999')

    assert res.status_code == 404
    assert res.json == {"error": "Menu item not found"}
