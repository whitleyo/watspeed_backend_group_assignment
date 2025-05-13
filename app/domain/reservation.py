from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from typing import Optional
from datetime import datetime

Base = declarative_base()

class Reservation(Base):
    """
    SQLAlchemy model for table reservations.
    """
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    table_id: Mapped[int] = mapped_column(Integer, ForeignKey("tables.id"), nullable=False)
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    people_count: Mapped[int] = mapped_column(Integer, nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def __init__(
        self,
        table_id: int,
        customer_name: str,
        people_count: int,
        time: datetime
    ):
        self.table_id = table_id
        self.customer_name = customer_name
        self.people_count = people_count
        self.time = time

    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            "id": self.id,
            "table_id": self.table_id,
            "customer_name": self.customer_name,
            "people_count": self.people_count,
            "time": self.time.isoformat() if self.time else None
        }

