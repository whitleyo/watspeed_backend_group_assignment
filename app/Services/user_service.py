from typing import Optional, List
from app.domain.user import User
from app.daos.user_dao import UserDAO

class UserService:
    """
    Service layer for handling user-related business logic.
    """

    def __init__(self, user_dao: UserDAO):
        """
        Initialize the service with a UserDAO instance.
        """
        self.user_dao = user_dao

    def get_user(self, user_id: int) -> Optional[User]:
        """
        Get a user by ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            Optional[User]: The user object if found, otherwise None.
        """
        return self.user_dao.find(user_id)

    def get_all_users(self) -> List[User]:
        """
        Get all users.

        Returns:
            List[User]: A list of all user objects.
        """
        return self.user_dao.findAll()

    def create_user(self, username: str, email: str) -> User:
        """
        Create a new user.

        Args:
            username (str): The username of the user.
            email (str): The email address of the user.

        Returns:
            User: The created user object.
        """
        new_user = User(user_id=0, username=username, email=email)
        return self.user_dao.save(0, new_user)

    def update_user(self, user_id: int, username: Optional[str] = None, email: Optional[str] = None) -> Optional[User]:
        """
        Update an existing user's details.

        Args:
            user_id (int): The ID of the user to update.
            username (Optional[str]): The new username (if provided).
            email (Optional[str]): The new email address (if provided).

        Returns:
            Optional[User]: The updated user object if found, otherwise None.
        """
        user = self.user_dao.find(user_id)
        if not user:
            return None
        
        if username is None and email is None:
            return user

        if username:
            user.username = username
        if email:
            user.email = email

        return self.user_dao.save(user_id, user)

    def delete_user(self, user_id: int) -> None:
        """
        Delete a user by ID.

        Args:
            user_id (int): The ID of the user to delete.
        """
        self.user_dao.delete(user_id)
