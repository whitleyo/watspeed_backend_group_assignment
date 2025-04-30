import unittest
from unittest.mock import MagicMock
from app.Services.user_service import UserService
from app.domain.user import User

class TestUserService(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment with a mocked UserDAO and UserService.
        """
        self.mock_user_dao = MagicMock()
        self.user_service = UserService(user_dao=self.mock_user_dao)

    def test_get_user_success(self):
        """
        Test retrieving a user by ID successfully.
        """
        # Arrange
        user = User(user_id=1, username="john_doe", email="john@example.com")
        self.mock_user_dao.find.return_value = user

        # Act
        result = self.user_service.get_user(1)

        # Assert
        self.assertEqual(result, user)
        self.mock_user_dao.find.assert_called_once_with(1)

    def test_get_user_not_found(self):
        """
        Test retrieving a user by ID when the user does not exist.
        """
        # Arrange
        self.mock_user_dao.find.return_value = None

        # Act
        result = self.user_service.get_user(999)

        # Assert
        self.assertIsNone(result)
        self.mock_user_dao.find.assert_called_once_with(999)

    def test_get_all_users(self):
        """
        Test retrieving all users.
        """
        # Arrange
        users = [
            User(user_id=1, username="john_doe", email="john@example.com"),
            User(user_id=2, username="jane_doe", email="jane@example.com")
        ]
        self.mock_user_dao.findAll.return_value = users

        # Act
        result = self.user_service.get_all_users()

        # Assert
        self.assertEqual(result, users)
        self.mock_user_dao.findAll.assert_called_once()

    def test_get_all_users_no_users(self):
        """
        Test retrieving all users when no users exist.
        """
        # Arrange
        self.mock_user_dao.findAll.return_value = []

        # Act
        result = self.user_service.get_all_users()

        # Assert
        self.assertEqual(result, [])
        self.mock_user_dao.findAll.assert_called_once()
    
    def test_create_user(self):
        """
        Test creating a new user.
        """
        # Arrange
        user = User(user_id=0, username="john_doe", email="john@example.com")
        saved_user = User(user_id=1, username="john_doe", email="john@example.com")
        self.mock_user_dao.save.return_value = saved_user

        # Act
        result = self.user_service.create_user("john_doe", "john@example.com")

        # Assert
        self.assertEqual(result, saved_user)

    def test_create_user_duplicate_username(self):
        """
        Test creating a user with a duplicate username.
        """
        # Arrange
        existing_user = User(user_id=1, username="john_doe", email="john@example.com")
        self.mock_user_dao.findAll.return_value = [existing_user]

        # Act
        result = self.user_service.create_user("john_doe", "john2@example.com")

        # Assert
        self.assertIsNone(result)
        self.mock_user_dao.findAll.assert_called_once()
        self.mock_user_dao.save.assert_not_called()

    def test_update_user_success(self):
        """
        Test updating an existing user's details successfully.
        """
        # Arrange
        user = User(user_id=1, username="john_doe", email="john@example.com")
        updated_user = User(user_id=1, username="john_updated", email="john_updated@example.com")
        self.mock_user_dao.find.return_value = user
        self.mock_user_dao.save.return_value = updated_user

        # Act
        result = self.user_service.update_user(1, username="john_updated", email="john_updated@example.com")

        # Assert
        self.assertEqual(result, updated_user)
        self.mock_user_dao.find.assert_called_once_with(1)
        self.mock_user_dao.save.assert_called_once_with(1, user)

    def test_update_user_no_changes(self):
        """
        Test updating a user with no changes (both username and email are None).
        """
        # Arrange
        user = User(user_id=1, username="john_doe", email="john@example.com")
        self.mock_user_dao.find.return_value = user

        # Act
        result = self.user_service.update_user(1)

        # Assert
        self.assertEqual(result, user)
        self.mock_user_dao.find.assert_called_once_with(1)
        self.mock_user_dao.save.assert_not_called()

    def test_update_user_not_found(self):
        """
        Test updating a user that does not exist.
        """
        # Arrange
        self.mock_user_dao.find.return_value = None

        # Act
        result = self.user_service.update_user(999, username="new_username")

        # Assert
        self.assertIsNone(result)
        self.mock_user_dao.find.assert_called_once_with(999)
        self.mock_user_dao.save.assert_not_called()

    def test_delete_user(self):
        """
        Test deleting a user by ID.
        """
        # Arrange
        user = User(user_id=1, username="john_doe", email="john@example.com")
        self.mock_user_dao.find.return_value = user

        # Act
        self.user_service.delete_user(1)

        # Assert
        self.mock_user_dao.delete.assert_called_once_with(1)
