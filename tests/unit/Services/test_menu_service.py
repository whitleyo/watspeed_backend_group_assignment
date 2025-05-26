import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.domain.menu_item import MenuItem, Base
from app.Services.menu_service import MenuService
from app.daos.menu_dao import MenuDAO
import io

# Test database setup
TEST_DB_URL = "postgresql://test_user:test_password@localhost/test_db"
engine = create_engine(TEST_DB_URL)
Session = sessionmaker(bind=engine)

@pytest.fixture(scope="module")
def setup_database():
    """Sets up the test database before running tests."""
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

@pytest.fixture(autouse=True)
def clean_menu_items(db_session):
    db_session.query(MenuItem).delete()
    db_session.commit()

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
        size="Medium",
        price=3.0
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
        description="Very dark coffee",
        size="Large",
        price=3.5
    )
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    return item

@pytest.fixture
def sample_menu_item3(db_session):
    """Creates and stores another sample menu item in the test database."""
    item = MenuItem(
        name="Dark Espresso",
        description="Very dark coffee",
        size="Small",
        price=1.25
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
    assert result.name == sample_menu_item.name
    assert result.size == sample_menu_item.size
    assert result.price == sample_menu_item.price

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
    assert result[0].name == sample_menu_item.name
    assert result[1].name == sample_menu_item2.name

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

def test_unique_ids_for_same_type_items(menu_dao, sample_menu_item2, sample_menu_item3):
    """Test that items of the same type but different sizes get unique IDs."""
    service = MenuService(menu_dao)

    espresso_medium = sample_menu_item2  # Dark Espresso, Large
    espresso_small = sample_menu_item3   # Dark Espresso, Small

    assert espresso_medium.id != espresso_small.id  # IDs should be unique
    assert espresso_medium.name == espresso_small.name  # Same name
    assert espresso_medium.size != espresso_small.size  # Different sizes

def test_update_non_existent_menu_item(menu_dao):
    """Test updating a non-existent menu item."""
    service = MenuService(menu_dao)

    updated_item = MenuItem(
        name="Non-existent Espresso",
        description="This should not exist",
        size="Medium",
        price=3.0
    )

    result = service.update_menu_item(999, updated_item)
    assert result is None  # No update should occur

# ---- Deletion Tests ----
def test_delete_menu_item(menu_dao, sample_menu_item):
    """Test deleting a menu item."""
    service = MenuService(menu_dao)
    service.remove_menu_item(sample_menu_item.id)

    assert menu_dao.find(sample_menu_item.id) is None  # Ensures deletion

def test_delete_non_existent_menu_item(menu_dao):
    """Test deleting a non-existent menu item."""
    service = MenuService(menu_dao)
    result = service.remove_menu_item(999)  # Non-existent ID

    assert result is None  # No deletion should occur

def test_generate_menu_pdf(menu_dao):
    """
    Test that generate_menu_pdf returns a non-empty PDF bytes object.
    """
    service = MenuService(menu_dao)
    pdf_bytes = service.generate_menu_pdf()

    # Check that the result is bytes and not empty
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 100  # Should be more than just a PDF header

    # Optionally, check that the PDF header is present
    assert pdf_bytes.startswith(b'%PDF')
