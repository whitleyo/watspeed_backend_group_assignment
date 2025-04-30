class User:
    def __init__(self, user_id: int, username: str, email: str):
        """
        Initializes a new User instance.

        Args:
            user_id (int): The unique identifier for the user.
            username (str): The username of the user.
            email (str): The email address of the user.
        """
        self.user_id: int = user_id  # Unique identifier for the user
        self.username: str = username  # Username of the user
        self.email: str = email  # Email address of the user
