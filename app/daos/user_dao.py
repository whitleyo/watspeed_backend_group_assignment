from app.domain.user import User
from app.daos.dao_abs import DAO
from typing import List, Optional
from db.database import get_session
from sqlalchemy.orm import Session

class UserDAO(DAO):
    """
    Data Access Object (DAO) for managing User entities using SQLAlchemy.
    """

    def __init__(self, session: Optional[Session] = None):
        """Initialize with an active database session."""
        if session is None:
            self.session = get_session()
        else:
            self.session = session

    def find(self, user_id: int) -> Optional[User]:
        """Retrieve a user by their ID."""
        return self.session.get(User, user_id)

    def findAll(self) -> List[User]:
        """Retrieve all users."""
        return self.session.query(User).all()

    def find_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by their username."""
        return self.session.query(User).filter(User.username == username).first()

    def save(self, user: User) -> User:
        """Save a new user."""
        try:
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error saving user: {e}")

    def update(self, user_id: int, updated_user: User) -> User:
        """Update an existing user."""
        user = self.session.get(User, user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} does not exist.")

        user.username = updated_user.username
        user.email = updated_user.email
        user.password = updated_user.password  # Ensure hashed password in production

        try:
            self.session.commit()
            self.session.refresh(user)
            return user
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error updating user: {e}")

    def delete(self, user_id: int) -> None:
        """Delete a user by ID."""
        user = self.session.get(User, user_id)
        if user:
            try:
                self.session.delete(user)
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                raise ValueError(f"Error deleting user: {e}")
