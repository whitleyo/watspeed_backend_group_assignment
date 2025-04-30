from typing import List, Optional
from app.domain.menu_item import MenuItem

class MenuDAO:
    """
    Data Access Object (DAO) for managing menu items.
    """

    def __init__(self):
        # Simulated in-memory database
        self.menu_items = {}
        self.next_id = 1  # Auto-incrementing ID for new items

    def find(self, item_id: int) -> Optional[MenuItem]:
        """Retrieve a menu item by its ID."""
        return self.menu_items.get(item_id)

    def findAll(self) -> List[MenuItem]:
        """Retrieve all menu items."""
        return list(self.menu_items.values())

    def save(self, item_id: int, menu_item: MenuItem) -> MenuItem:
        """
        Save a new or updated menu item.
        - If `item_id == 0`, create a new item with a unique ID.
        - Otherwise, update an existing item.
        """
        if item_id == 0:
            item_id = self.next_id
            self.next_id += 1
        
        new_menu_item = MenuItem(
            id=item_id,
            name=menu_item.name,
            description=menu_item.description,
            sizes=menu_item.sizes,
            prices=menu_item.prices
        )
        self.menu_items[item_id] = new_menu_item
        return new_menu_item

    def delete(self, item_id: int) -> None:
        """Delete a menu item by ID; no return value."""
        self.menu_items.pop(item_id, None)