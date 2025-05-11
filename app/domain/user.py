from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """
    SQLAlchemy model for users.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)  # Stores hashed password

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password  # Store hashed password in production!

    def to_dict(self):
        """Convert model instance to dictionary (excluding password for security)."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }
