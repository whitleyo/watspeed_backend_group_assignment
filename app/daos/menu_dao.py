from typing import List, Optional
from ..domain.menu_item import MenuItem
from .dao_abs import DAO
from db.database import get_session
from typing import List, Optional
from app.domain.menu_item import MenuItem

class MenuDAO(DAO):
    """
    Data Access Object (DAO) for managing menu items using SQLAlchemy with an active session.
    """

    def __init__(self):
        """Initialize with an active database session."""
        self.session = get_session()

    def find(self, item_id: int) -> Optional[MenuItem]:
        """Retrieve a menu item by its ID."""
        return self.session.get(MenuItem, item_id)

    def findAll(self) -> List[MenuItem]:
        """Retrieve all menu items."""
        return self.session.query(MenuItem).all()

    def save(self, menu_item: MenuItem) -> MenuItem:
        """Save a new menu item."""
        try:
            self.session.add(menu_item)
            self.session.commit()
            self.session.refresh(menu_item)
            return menu_item
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error saving menu item: {e}")

    def update(self, item_id: int, updated_item: MenuItem) -> MenuItem:
        """Update an existing menu item."""
        menu_item = self.session.get(MenuItem, item_id)
        if not menu_item:
            raise ValueError(f"Menu item with ID {item_id} does not exist.")

        menu_item.name = updated_item.name
        menu_item.description = updated_item.description
        menu_item.size = updated_item.size
        menu_item.price = updated_item.price

        try:
            self.session.commit()
            self.session.refresh(menu_item)
            return menu_item
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error updating menu item: {e}")

    def delete(self, item_id: int) -> None:
        """Delete a menu item by ID."""
        menu_item = self.session.get(MenuItem, item_id)
        if menu_item:
            try:
                self.session.delete(menu_item)
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                raise ValueError(f"Error deleting menu item: {e}")