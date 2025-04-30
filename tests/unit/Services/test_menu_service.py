import pytest
from unittest.mock import MagicMock
from app.domain.menu_item import MenuItem
from app.Services.menu_service import MenuService
from app.daos.menu_dao import MenuDAO

class TestMenuService:
    @pytest.fixture
    def mock_dao(self):
        """Create mock DAO for testing"""
        menu_dao = MagicMock(spec=MenuDAO)
        return menu_dao

    @pytest.fixture
    def sample_menu_item(self):
        """Sample menu item fixture"""
        return MenuItem(
            id=1,
            name="Espresso",
            description="Rich and bold coffee",
            sizes=["Small", "Medium", "Large"],
            prices={"Small": 2.5, "Medium": 3.0, "Large": 3.5}
        )

    # ---- Retrieval Tests ----
    def test_get_menu_item_success(self, mock_dao, sample_menu_item):
        """Test fetching a menu item successfully"""
        mock_dao.find.return_value = sample_menu_item
        service = MenuService(mock_dao)

        result = service.get_menu_item(1)
        assert result.id == 1
        assert result.name == "Espresso"
        mock_dao.find.assert_called_once_with(1)

    def test_get_menu_item_not_found(self, mock_dao):
        """Test fetching a non-existent menu item"""
        mock_dao.find.return_value = None
        service = MenuService(mock_dao)

        result = service.get_menu_item(999)
        assert result is None
        mock_dao.find.assert_called_once_with(999)

    def test_get_all_menu_items(self, mock_dao, sample_menu_item):
        """Test retrieving all menu items"""
        mock_dao.findAll.return_value = [sample_menu_item]
        service = MenuService(mock_dao)

        result = service.get_all_menu_items()
        assert len(result) == 1
        assert result[0].name == "Espresso"
        mock_dao.findAll.assert_called_once()

    # ---- Creation & Updating Tests ----
    def test_create_menu_item(self, mock_dao, sample_menu_item):
        """Test creating a new menu item"""
        mock_dao.save.return_value = sample_menu_item
        service = MenuService(mock_dao)

        new_item = MenuItem(
            id=0,  # New item
            name="Latte",
            description="Creamy milk coffee",
            sizes=["Medium", "Large"],
            prices={"Medium": 4.0, "Large": 4.5}
        )
        result = service.add_or_update_menu_item(0, new_item)

        assert result.name == "Latte"
        mock_dao.save.assert_called_once()

    def test_update_existing_menu_item(self, mock_dao, sample_menu_item):
        """Test updating an existing menu item"""
        mock_dao.save.return_value = sample_menu_item
        service = MenuService(mock_dao)

        updated_item = MenuItem(
            id=1,
            name="Updated Espresso",
            description="Stronger coffee",
            sizes=["Small", "Medium"],
            prices={"Small": 2.8, "Medium": 3.3}
        )
        result = service.add_or_update_menu_item(1, updated_item)

        assert result.name == "Updated Espresso"
        mock_dao.save.assert_called_once()

    # ---- Deletion Tests ----
    def test_delete_menu_item(self, mock_dao):
        """Test deleting a menu item"""
        service = MenuService(mock_dao)
        service.remove_menu_item(1)

        mock_dao.delete.assert_called_once_with(1)

