import pytest
from flask import Flask, json
from unittest.mock import MagicMock
from app.Services.menu_service import MenuService
from app.domain.menu_item import MenuItem
from app.Routes.menu import bp  # Import the menu routes
import app

class TestMenuRoutes:
    """Test class for menu route endpoints."""

    @classmethod
    def setup_class(cls):
        """Set up Flask test client and mock dependency injection."""
        from app import create_app
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.mock_service = MagicMock(spec=MenuService)

        # Override dependency injection globally for all tests
        def mock_binder(binder):
            binder.bind(MenuService, to=cls.mock_service)

        from injector import Injector
        from flask_injector import FlaskInjector
        cls.injector = Injector([mock_binder])
        FlaskInjector(app=cls.app, injector=cls.injector)

    @pytest.fixture
    def sample_menu_item(self):
        """Sample menu item fixture."""
        return MenuItem(
            id=1,
            name="Cappuccino",
            description="Frothy and smooth coffee",
            sizes=["Small", "Medium", "Large"],
            prices={"Small": 3.5, "Medium": 4.0, "Large": 4.5}
        )

    # ---- Retrieval Tests ----
    def test_get_all_menu_items_success(self, sample_menu_item):
        """Test retrieving all menu items."""
        self.mock_service.get_all_menu_items.return_value = [sample_menu_item]

        res = self.client.get('/menu/')
        assert res.status_code == 200
        assert len(res.json) == 1
        assert res.json[0]["name"] == "Cappuccino"

    def test_get_menu_item_success(self, sample_menu_item):
        """Test retrieving a specific menu item."""
        self.mock_service.get_menu_item.return_value = sample_menu_item

        res = self.client.get('/menu/1')
        assert res.status_code == 200
        assert res.json["name"] == "Cappuccino"

    def test_get_menu_item_not_found(self):
        """Test retrieving a non-existent menu item."""
        self.mock_service.get_menu_item.return_value = None

        res = self.client.get('/menu/999')
        assert res.status_code == 404
        assert res.json == {"error": "Menu item not found"}

    # ---- Creation & Updating Tests ----
    def test_create_menu_item_success(self, sample_menu_item):
        """Test creating a new menu item."""
        self.mock_service.add_or_update_menu_item.return_value = sample_menu_item

        data = {
            "name": "Latte",
            "description": "Milk coffee",
            "sizes": ["Small", "Medium"],
            "prices": {"Small": 3.8, "Medium": 4.2}
        }
        res = self.client.post('/menu/', json=data)

        assert res.status_code == 201
        assert res.json["name"] == "Cappuccino"  # Mock returns sample item

    def test_update_menu_item_success(self, sample_menu_item):
        """Test updating an existing menu item."""
        self.mock_service.get_menu_item.return_value = sample_menu_item
        self.mock_service.add_or_update_menu_item.return_value = sample_menu_item

        data = {"name": "Updated Cappuccino", "description": "Stronger coffee"}
        res = self.client.put('/menu/1', json=data)

        assert res.status_code == 200
        assert res.json["name"] == "Cappuccino"  # Mocked response

    # ---- Deletion Tests ----
    def test_delete_menu_item_success(self, sample_menu_item):
        """Test deleting a menu item."""
        self.mock_service.get_menu_item.return_value = sample_menu_item
        self.mock_service.remove_menu_item.return_value = None

        res = self.client.delete('/menu/1')

        assert res.status_code == 200
        assert res.json == {"message": "Menu item deleted"}

    def test_delete_menu_item_not_found(self):
        """Test deleting a non-existent menu item."""
        self.mock_service.get_menu_item.return_value = None

        res = self.client.delete('/menu/999')

        assert res.status_code == 404
        assert res.json == {"error": "Menu item not found"}
