from typing import List, Optional
from app.daos.menu_dao import MenuDAO
from app.domain.menu_item import MenuItem
from app.messages.responses.menu_item_response_dto import MenuItemResponseDTO
from app.mappers.menu_mapper import menu_item_to_response, menu_list_to_response

class MenuService:
    """
    Service layer for managing menu operations.
    """

    def __init__(self, menu_dao: MenuDAO):
        """Initialize service with DAO."""
        self.menu_dao = menu_dao

    def get_menu_item(self, item_id: int) -> Optional[MenuItemResponseDTO]:
        """Retrieve menu item by ID and convert to response DTO."""
        menu_item = self.menu_dao.find(item_id)
        return menu_item_to_response(menu_item) if menu_item else None

    def get_all_menu_items(self) -> List[MenuItemResponseDTO]:
        """Retrieve all menu items and convert them to DTOs."""
        menu_items = self.menu_dao.findAll()
        return menu_list_to_response(menu_items)

    def add_or_update_menu_item(self, item_id: int, menu_item: MenuItem) -> MenuItemResponseDTO:
        """Add or update a menu item and return response DTO."""
        saved_item = self.menu_dao.save(item_id, menu_item)
        return menu_item_to_response(saved_item)

    def remove_menu_item(self, item_id: int) -> None:
        """Delete a menu item."""
        self.menu_dao.delete(item_id)
