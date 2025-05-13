from typing import List, Optional
from ..domain.order import Order  # Assuming you have an Order domain class
from .dao_abs import DAO
from db.database import get_session

class OrderDAO(DAO):
    """DAO for managing orders."""

    def __init__(self):
        self.session = get_session()

    def find(self, order_id: int) -> Optional[Order]:
        """Retrieve an order by ID."""
        return self.session.get(Order, order_id)

    def findAll(self) -> List[Order]:
        """Retrieve all orders."""
        return self.session.query(Order).all()

    def save(self, order: Order) -> Order:
        """Save a new order."""
        try:
            self.session.add(order)
            self.session.commit()
            self.session.refresh(order)
            return order
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error saving order: {e}")

    def update(self, order_id: int, updated_order: Order) -> Order:
        """Update an existing order."""
        order = self.session.get(Order, order_id)
        if not order:
            raise ValueError(f"Order with ID {order_id} does not exist.")

        order.customer_name = updated_order.customer_name
        order.menu_id = updated_order.menu_id
        order.quantity = updated_order.quantity
        order.order_time = updated_order.order_time

        try:
            self.session.commit()
            self.session.refresh(order)
            return order
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error updating order: {e}")

    def delete(self, order_id: int) -> None:
        """Delete an order by ID."""
        order = self.session.get(Order, order_id)
        if order:
            try:
                self.session.delete(order)
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                raise ValueError(f"Error deleting order: {e}")

    