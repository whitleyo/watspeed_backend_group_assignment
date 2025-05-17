from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from app.domain.base import Base
from typing import Optional, List
from datetime import datetime

# Association table linking orders to multiple menu items
order_menu_items = Table(
    "order_menu_items",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id"), primary_key=True),
    Column("menu_id", Integer, ForeignKey("menu.id"), primary_key=True),
)

class Order(Base):
    """
    SQLAlchemy model for customer orders.
    """
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    order_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def __init__(
        self, 
        customer_name: str, 
        menu_items: List["MenuItem"], 
        quantity: int, 
        order_time: Optional[datetime] = None
    ):
        self.customer_name = customer_name
        self.menu_items = menu_items  # Store multiple menu items in a list
        self.quantity = quantity
        self.order_time = order_time if order_time else datetime.now()

    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "menu_items": [item.to_dict() for item in self.menu_items],  # Get all linked menu items
            "quantity": self.quantity,
            "status": self.status,
            "order_time": self.order_time.isoformat() if self.order_time else None
        }

