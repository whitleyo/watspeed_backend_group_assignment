from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
# from ..domain.order import Order
from typing import List, Optional

Base = declarative_base()

class MenuItem(Base):
    """
    SQLAlchemy model for menu items.
    """
    __tablename__ = "menu"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    size: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL(5,2), nullable=False)

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
