from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Table(Base):
    """
    SQLAlchemy model for tables.
    """
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)

    def __init__(self, capacity: int, location: str):
        self.capacity = capacity
        self.location = location

    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            "id": self.id,
            "capacity": self.capacity,
            "location": self.location
        }