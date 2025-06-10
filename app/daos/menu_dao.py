from app.domain.menu_item import MenuItem
from app.daos.dao_abs import DAO
from typing import List, Optional
from db.database import get_session
from sqlalchemy.orm import Session

class MenuDAO(DAO):
    """
    Data Access Object (DAO) for managing menu items using SQLAlchemy with an active session.
    """

    def __init__(self, session: Optional[Session] = None):
        if session is None:
            self.session = get_session()
        else:
            self.session = session

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
            print(f"Menu item with ID {item_id} does not exist.")
            return None

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
        else:
            print(f"Menu item with ID {item_id} does not exist.")