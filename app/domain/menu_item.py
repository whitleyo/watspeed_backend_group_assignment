from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DECIMAL
from sqlalchemy.orm import declarative_base
from sqlalchemy import UniqueConstraint
# from ..domain.order import Order

Base = declarative_base()

class MenuItem(Base):
    """
    SQLAlchemy model for menu items.
    """
    __tablename__ = "menu"
    __table_args__ = (UniqueConstraint("name", "size", name="unique_menu_item"),)

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
