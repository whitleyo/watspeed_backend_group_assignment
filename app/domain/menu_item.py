from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DECIMAL, UniqueConstraint
from typing import List
from .base import Base  # Assuming your base class is in base.py

class MenuItem(Base):
    """
    SQLAlchemy model for menu items.
    """
    __tablename__ = "menu"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    size: Mapped[str] = mapped_column(String(50), nullable=True)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)

    # Track order items with quantity
    order_items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="menu_item")

    def __init__(self, name: str, description: str, size: str, price: float):
        self.name = name
        self.description = description
        self.size = size
        self.price = price

    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "size": self.size,
            "price": float(self.price)  # Convert Decimal to float
        }