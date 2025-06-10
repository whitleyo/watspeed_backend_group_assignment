from typing import List, Optional
from sqlalchemy.orm import Session
from ..domain.order import Order, OrderItem  # Import Order and OrderItem models
from ..domain.menu_item import MenuItem  # Import MenuItem for validation
from .dao_abs import DAO
from db.database import get_session

class OrderDAO(DAO):
    """DAO for managing orders."""

    def __init__(self, session: Optional[Session] = None):
        """Initialize OrderDAO with an optional session."""
        self.session = session if session else get_session()

    def find(self, order_id: int) -> Optional[Order]:
        """Retrieve an order by ID."""
        return self.session.get(Order, order_id)

    def findAll(self) -> List[Order]:
        """Retrieve all orders."""
        return self.session.query(Order).all()

    def get_menu_items_by_ids(self, menu_item_ids: List[int]) -> List[MenuItem]:
        """Fetches valid menu items based on provided IDs."""
        return self.session.query(MenuItem).filter(MenuItem.id.in_(menu_item_ids)).all()

    def save(self, order: Order) -> Order:
        """
        Saves an order along with its associated order items.
        """
        try:
            # Validate menu items before committing
            menu_item_ids = {item.menu_item_id for item in order.order_items}
            menu_items = self.get_menu_items_by_ids(list(menu_item_ids))

            existing_ids = {item.id for item in menu_items}
            invalid_ids = [item_id for item_id in menu_item_ids if item_id not in existing_ids]

            if invalid_ids:
                raise ValueError(f"Invalid menu item IDs: {invalid_ids}")

            # Persist order & relationships
            self.session.add(order)
            self.session.commit()
            self.session.refresh(order)

            return order
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error saving order: {e}")

    def update(self, order_id: int, updated_order: Order) -> Order:
        """Updates an existing order, ensuring order items are correctly replaced."""
        order = self.session.get(Order, order_id)
        if not order:
            raise ValueError(f"Order with ID {order_id} does not exist.")

        try:
            # Remove old order items
            self.session.query(OrderItem).filter(OrderItem.order_id == order_id).delete()

            # # Ensure updated_order.order_items is correctly populated
            # print(f"Before assigning new items - updated_order.order_items: {updated_order.order_items}")

            # Add new menu items using method
            order.add_menu_items({item.menu_item_id: item.quantity for item in updated_order.order_items})

            # print(f"After assigning new items - order.order_items: {order.order_items}")

            order.customer_name = updated_order.customer_name
            order.status = updated_order.status

            self.session.commit()
            self.session.refresh(order)

            # print(f"After commit - order.order_items: {order.order_items}")  # Debugging

            return order
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error updating order: {e}")

    def delete(self, order_id: int) -> None:
        """Delete an order and its associated order items."""
        order = self.session.get(Order, order_id)
        if not order:
            raise ValueError(f"Order with ID {order_id} does not exist.")

        try:
            # First, delete associated `OrderItem` entries
            self.session.query(OrderItem).filter(OrderItem.order_id == order_id).delete()

            # Now delete the order itself
            self.session.delete(order)

            # Commit both deletions
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error deleting order: {e}")