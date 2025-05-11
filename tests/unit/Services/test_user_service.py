import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.domain.user import Base, User
from app.services.user_service import UserService
from app.daos.user_dao import UserDAO

# Test database URL
TEST_DB_URL = "postgresql://test_user:test_password@localhost/test_db"
engine = create_engine(TEST_DB_URL)
Session = sessionmaker(bind=engine)

@pytest.fixture(scope="session")
def setup_database():
    """Ensures the test database follows the strict schema before tests."""
    Base.metadata.create_all(engine)  # Create tables
    yield
    Base.metadata.drop_all(engine)  # Cleanup after tests

@pytest.fixture(scope="function")
def db_session(setup_database):
    """Provides a fresh database session for each test."""
    session = Session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def user_dao(db_session):
    """Provides an instance of UserDAO with a test DB session."""
    return UserDAO(db_session)

@pytest.fixture
def sample_user(db_session):
    """Creates and stores a sample user in the test database."""
    user = User(username="john_doe", email="john@example.com", password="hashed_password")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def sample_user2(db_session):
    """Creates and stores another sample user in the test database."""
    user = User(username="jane_doe", email="jane@example.com", password="hashed_password")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

# ---- Retrieval Tests ----
def test_get_user_success(user_dao, sample_user):
    """Test fetching a user successfully."""
    service = UserService(user_dao)
    result = service.get_user(sample_user.id)

    assert result.id == sample_user.id
    assert result.username == "john_doe"
    assert result.email == "john@example.com"

def test_get_user_not_found(user_dao):
    """Test fetching a non-existent user."""
    service = UserService(user_dao)
    result = service.get_user(999)
    assert result is None

def test_get_all_users(user_dao, sample_user, sample_user2):
    """Test retrieving all users."""
    service = UserService(user_dao)
    result = service.get_all_users()

    assert len(result) == 2
    assert isinstance(result[0], User)
    assert isinstance(result[1], User)

def test_get_all_users_no_users(user_dao):
    """Test retrieving users when none exist."""
    service = UserService(user_dao)
    result = service.get_all_users()
    assert len(result) == 0  # Database starts empty for this test

# ---- User Creation Tests ----
def test_create_user(user_dao, db_session):
    """Test creating a new user."""
    service = UserService(user_dao)
    new_user = User(username="new_user", email="new@example.com", password="hashed_password")

    result = service.create_user("new_user", "new@example.com", "hashed_password")

    assert result.username == "new_user"
    assert result.email == "new@example.com"
    assert result.id is not None  # Auto-incremented ID

def test_create_user_duplicate_username(user_dao, sample_user):
    """Test creating a user with a duplicate username."""
    service = UserService(user_dao)
    result = service.create_user("john_doe", "duplicate@example.com", "hashed_password")

    assert result is None  # Username already taken

# ---- User Update Tests ----
def test_update_user_success(user_dao, sample_user):
    """Test updating an existing user's details."""
    service = UserService(user_dao)
    updated_user = User(username="updated_user", email="updated@example.com", password="new_password")

    result = service.update_user(sample_user.id, updated_user)

    assert result.username == "updated_user"
    assert result.email == "updated@example.com"

def test_update_user_not_found(user_dao):
    """Test updating a user that doesn't exist."""
    service = UserService(user_dao)
    updated_user = User(username="new_name", email="new@example.com", password="new_password")

    result = service.update_user(999, updated_user)

    assert result is None  # User not found

# ---- User Deletion Tests ----
def test_delete_user(user_dao, sample_user):
    """Test deleting a user."""
    service = UserService(user_dao)
    service.delete_user(sample_user.id)

    assert user_dao.find(sample_user.id) is None  # User should no longer exist

