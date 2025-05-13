from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from typing import Optional
from datetime import datetime

Base = declarative_base()

class Order(Base):
    """
    SQLAlchemy model for customer orders.
    """
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    menu_id: Mapped[int] = mapped_column(Integer, ForeignKey("menu.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    order_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def __init__(
        self, 
        customer_name: str, 
        menu_id: int, 
        quantity: int, 
        order_time: Optional[datetime] = None
    ):
        self.customer_name = customer_name
        self.menu_id = menu_id
        self.quantity = quantity
        self.order_time = order_time if order_time else datetime.now()

    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "menu_id": self.menu_id,
            "quantity": self.quantity,
            "order_time": self.order_time.isoformat() if self.order_time else None
        }

