from datetime import datetime
from typing import List, Optional
from ..domain.order import Order
from .dao_abs import DAO

class OrderDAO(DAO):
    def __init__(self):
        self.orders = {}  # Simulated database with order_id as the key
        self.next_id = 1  # Simulated ID generator

    def find(self, order_id: int) -> Optional[Order]:
        return self.orders.get(order_id)

    def findAll(self) -> List[Order]:
        return list(self.orders.values())

    def save(self, order: Order) -> Order:
        now = datetime.now()
         # Create new order
        order.id = self.next_id
        self.next_id += 1
        order.timestamp = now.strftime("%Y-%m-%d %H:%M:%S")  # Timestamp
        self.orders[order.id] = order
        return order

    def update(self, order_id: int, order: Order) -> Order:
        now = datetime.now()
        # update existing order
        existing_order = self.find(order_id)
        if existing_order is None:
            raise ValueError(f"Order with ID {order_id} does not exist.")
        else:
            # Update the existing order with new values
        
            existing_order.items = order.items
            existing_order.size = order.size
            existing_order.status = order.status
            existing_order.timestamp = now.strftime("%Y-%m-%d %H:%M:%S")  # Timestamp
              
        return existing_order

    def delete(self, order_id: int):
        found_order = self.find(order_id)  # Check if order exists
        if found_order:
            self.orders.pop(order_id, None)
            return True
        else:
            return False