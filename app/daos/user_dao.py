from typing import Optional, List
from app.domain.user import User

class UserDAO:
    """
    Data Access Object (DAO) for managing User entities.
    """

    def __init__(self):
        # In-memory storage for simplicity (replace with database logic in production)
        self.users: List[User] = [
            User(1, "ilovecoffee", "cafegirl@gmail.com"),
            User(2, "ilovetea", "teagirl@hotmail.com")]
        self.next_id: int = 3  # Auto-incrementing ID for new users

    def find(self, user_id: int) -> Optional[User]:
        """
        Return the object with the specified ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            Optional[User]: The user object if found, otherwise None.
        """
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def findAll(self) -> List[User]:
        """
        Return an array of all objects.

        Returns:
            List[User]: A list of all user objects.
        """
        return self.users

    def save(self, user_id: int, user: User) -> User:
        """
        Save the object with the given ID. If ID is zero, create a new object.

        Args:
            user_id (int): The ID of the user to save.
            user (User): The user object to save.

        Returns:
            User: The saved user object with a non-zero ID.
        """
        if user_id == 0:
            # Create a new user
            user.user_id = self.next_id
            self.users.append(user)
            self.next_id += 1
        else:
            # Update an existing user
            existing_user = self.find(user_id)
            if existing_user:
                existing_user.username = user.username
                existing_user.email = user.email
                existing_user.password = user.password
        return user

    def delete(self, user_id: int) -> None:
        """
        Delete the object with the given ID.

        Args:
            user_id (int): The ID of the user to delete.
        """
        user = self.find(user_id)
        if user:
            self.users.remove(user)
