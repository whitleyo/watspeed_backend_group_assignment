import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from app.domain.menu_item import MenuItem, Base
from app.Services.menu_service import MenuService
from app.daos.menu_dao import MenuDAO

# Test database URL
TEST_DB_URL = "postgresql://test_user:test_password@localhost/test_db"

# Create SQLAlchemy test database engine
engine = create_engine(TEST_DB_URL)
Session = sessionmaker(bind=engine)

@pytest.fixture(scope="module")
def setup_database():
    """Sets up the test database before running tests."""
    Base.metadata.create_all(engine)  # Create tables
    yield
    Base.metadata.drop_all(engine)  # Cleanup after tests

@pytest.fixture(scope="function")
def db_session(setup_database):
    """Provides a fresh database session for each test."""
    session = Session()
    yield session
    session.rollback()  # Rollback any test changes
    session.close()

@pytest.fixture
def menu_dao(db_session):
    """Provides an instance of MenuDAO with a test DB session."""
    return MenuDAO(db_session)

@pytest.fixture
def sample_menu_item(db_session):
    """Creates and stores a sample menu item in the test database."""
    item = MenuItem(
        name="Espresso",
        description="Rich and bold coffee",
        sizes=["Small", "Medium", "Large"],
        prices=[2.5, 3.0, 3.5]
    )
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    return item

@pytest.fixture
def sample_menu_item2(db_session):
    """Creates and stores another sample menu item in the test database."""
    item = MenuItem(
        name="Dark Espresso",
        description="Very Dark coffee",
        sizes=["Small", "Medium", "Large"],
        prices=[2.5, 3.0, 3.5]
    )
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    return item

# ---- Retrieval Tests ----
def test_get_menu_item_success(menu_dao, sample_menu_item):
    """Test fetching a menu item successfully."""
    service = MenuService(menu_dao)
    result = service.get_menu_item(sample_menu_item.id)

    assert result.id == sample_menu_item.id
    assert result.name == "Espresso"
    assert result.size == "Medium"
    assert result.price == 3.0

def test_get_menu_item_not_found(menu_dao):
    """Test fetching a non-existent menu item."""
    service = MenuService(menu_dao)
    result = service.get_menu_item(999)
    assert result is None

def test_get_all_menu_items(menu_dao, sample_menu_item, sample_menu_item2):
    """Test retrieving all menu items."""
    service = MenuService(menu_dao)
    result = service.get_all_menu_items()

    assert len(result) == 2
    assert result[0].name == "Espresso"
    assert result[1].name == "Dark Espresso"

# ---- Creation & Updating Tests ----
def test_create_menu_item(menu_dao):
    """Test creating a new menu item."""
    service = MenuService(menu_dao)

    new_item = MenuItem(
        name="Latte",
        description="Creamy milk coffee",
        size="Small",
        price=4.0
    )
    result = service.add_menu_item(new_item)

    assert result.name == "Latte"
    assert result.size == "Small"
    assert result.price == 4.0
    assert result.id is not None  # Auto-incrementing ID

def test_update_existing_menu_item(menu_dao, sample_menu_item):
    """Test updating an existing menu item."""
    service = MenuService(menu_dao)

    updated_item = MenuItem(
        name="Updated Espresso",
        description="Stronger coffee",
        size="Medium",
        price=3.3
    )

    result = service.update_menu_item(sample_menu_item.id, updated_item)

    assert result.name == "Updated Espresso"
    assert result.description == "Stronger coffee"
    assert result.id == sample_menu_item.id  # ID remains unchanged

# ---- Deletion Tests ----
def test_delete_menu_item(menu_dao, sample_menu_item):
    """Test deleting a menu item."""
    service = MenuService(menu_dao)
    service.remove_menu_item(sample_menu_item.id)

    assert menu_dao.find(sample_menu_item.id) is None  # Ensures deletion

