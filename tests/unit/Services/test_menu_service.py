import pytest
from app.domain.menu_item import MenuItem
from app.Services.menu_service import MenuService
from app.daos.menu_dao import MenuDAO

@pytest.fixture
def menu_dao():
    """Provides a simulated in-memory DAO instance"""
    return MenuDAO()

@pytest.fixture
def sample_menu_item(menu_dao):
    """Creates and stores a sample menu item in the simulated DAO"""
    item = MenuItem(
        id=0,  # Will be assigned a unique ID
        name="Espresso",
        description="Rich and bold coffee",
        sizes=["Small", "Medium", "Large"],
        prices={"Small": 2.5, "Medium": 3.0, "Large": 3.5}
    )
    return menu_dao.save(0, item)

@pytest.fixture
def sample_menu_item2(menu_dao):
    """Creates and stores another sample menu item in the simulated DAO"""
    item = MenuItem(
        id=0,  # Will be assigned a unique ID
        name="Dark Espresso",
        description="Very Dark coffee",
        sizes=["Small", "Medium", "Large"],
        prices={"Small": 2.5, "Medium": 3.0, "Large": 3.5}
    )
    return menu_dao.save(0, item)

# ---- Retrieval Tests ----
def test_get_menu_item_success(menu_dao, sample_menu_item):
    """Test fetching a menu item successfully"""
    service = MenuService(menu_dao)
    result = service.get_menu_item(sample_menu_item.id)

    assert result.id == sample_menu_item.id
    assert result.name == "Espresso"

def test_get_menu_item_not_found(menu_dao):
    """Test fetching a non-existent menu item"""
    service = MenuService(menu_dao)
    result = service.get_menu_item(999)
    assert result is None

def test_get_all_menu_items(menu_dao, sample_menu_item, sample_menu_item2):
    """Test retrieving all menu items"""
    service = MenuService(menu_dao)
    result = service.get_all_menu_items()
    
    assert len(result) == 2
    assert result[0].name == "Espresso"
    assert result[1].name == "Dark Espresso"

# ---- Creation & Updating Tests ----
def test_create_menu_item(menu_dao, sample_menu_item):
    """Test creating a new menu item"""
    service = MenuService(menu_dao)

    new_item = MenuItem(
        id=0,  # New item
        name="Latte",
        description="Creamy milk coffee",
        sizes=["Medium", "Large"],
        prices={"Medium": 4.0, "Large": 4.5}
    )
    result = service.add_or_update_menu_item(0, new_item)

    assert result.name == "Latte"
    assert result.id == 2  # Ensures auto-incrementing ID

def test_update_existing_menu_item(menu_dao, sample_menu_item):
    """Test updating an existing menu item"""
    service = MenuService(menu_dao)

    updated_item = MenuItem(
        id=sample_menu_item.id,  # Same ID to update existing item
        name="Updated Espresso",
        description="Stronger coffee",
        sizes=["Small", "Medium"],
        prices={"Small": 2.8, "Medium": 3.3}
    )

    result = service.add_or_update_menu_item(sample_menu_item.id, updated_item)

    assert result.name == "Updated Espresso"
    assert result.description == "Stronger coffee"
    assert result.id == sample_menu_item.id  # ID remains unchanged

# ---- Deletion Tests ----
def test_delete_menu_item(menu_dao, sample_menu_item):
    """Test deleting a menu item"""
    service = MenuService(menu_dao)
    service.remove_menu_item(sample_menu_item.id)

    assert menu_dao.find(sample_menu_item.id) is None  # Ensures deletio

