from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, ForeignKey, DECIMAL, Table, Column
from datetime import datetime
from typing import List, Optional
from .base import Base  # Assuming you have a base class defined in base.py

class OrderItem(Base):
    """
    Association table for Order and MenuItem with quantity tracking.
    """
    __tablename__ = "order_items"

    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True)
    menu_item_id: Mapped[int] = mapped_column(Integer, ForeignKey("menu.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships (Bidirectional)
    order: Mapped["Order"] = relationship("Order", back_populates="order_items")
    menu_item: Mapped["MenuItem"] = relationship("MenuItem", back_populates="order_items")

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    order_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    order_items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __init__(self, 
                customer_name: str, 
                order_time: Optional[datetime] = None, 
                items_data: Optional[dict] = None):
        """
        Initialize Order instance without menu items.
        """
        self.customer_name = customer_name
        self.status = "pending"
        self.order_time = order_time if order_time else datetime.now()
        # Initialize order_items as an empty list
        self.order_items = []
        # If items_data is provided, add menu items
        if items_data:
            self.add_menu_items(items_data)

    def add_menu_items(self, items_data: dict):
        """
        Add menu items from a dictionary where keys are menu_item_ids and values are quantities.
        """
        self.order_items = [
            OrderItem(order_id=self.id, menu_item_id=menu_item_id, quantity=quantity)
            for menu_item_id, quantity in items_data.items()
        ]

    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "status": self.status,
            "order_time": self.order_time.isoformat() if self.order_time else None,
            "order_items": [
                {"menu_item_id": item.menu_item.id, "quantity": item.quantity} for item in self.order_items
            ]
        }

