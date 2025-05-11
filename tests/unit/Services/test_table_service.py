import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.domain.table import Base, Table
from app.Services.table_service import TableService
from app.daos.table_dao import TableDAO

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
def table_dao(db_session):
    """Provides an instance of TableDAO with a test DB session."""
    return TableDAO(db_session)

@pytest.fixture
def sample_table(db_session):
    """Creates and stores a sample table in the test database."""
    table = Table(capacity=4, location="Downtown")
    db_session.add(table)
    db_session.commit()
    db_session.refresh(table)
    return table

@pytest.fixture
def sample_table2(db_session):
    """Creates and stores another sample table in the test database."""
    table = Table(capacity=6, location="Uptown")
    db_session.add(table)
    db_session.commit()
    db_session.refresh(table)
    return table

# ---- Retrieval Tests ----
def test_get_table_success(table_dao, sample_table):
    """Test fetching a table successfully."""
    service = TableService(table_dao)
    result = service.get_table(sample_table.id)

    assert result.id == sample_table.id
    assert result.capacity == 4
    assert result.location == "Downtown"

def test_get_table_not_found(table_dao):
    """Test fetching a non-existent table."""
    service = TableService(table_dao)
    result = service.get_table(999)
    assert result is None

def test_get_all_tables(table_dao, sample_table, sample_table2):
    """Test retrieving all tables."""
    service = TableService(table_dao)
    result = service.get_all_tables()

    assert len(result) == 2
    assert isinstance(result[0], Table)
    assert isinstance(result[1], Table)

# ---- Location-Specific Tests ----
def test_get_tables_by_location(table_dao, sample_table):
    """Test retrieving tables by location."""
    service = TableService(table_dao)
    result = service.get_tables_by_location("Downtown")

    assert len(result) == 1
    assert result[0].location == "Downtown"

def test_get_tables_by_nonexistent_location(table_dao):
    """Test retrieving tables from a non-existent location."""
    service = TableService(table_dao)
    result = service.get_tables_by_location("Nowhere")
    assert len(result) == 0

# ---- Capacity Tests ----
def test_get_table_capacity_success(table_dao, sample_table):
    """Test fetching table capacity."""
    service = TableService(table_dao)
    result = service.get_table_capacity(sample_table.id)

    assert result == 4

def test_get_table_capacity_not_found(table_dao):
    """Test fetching capacity for a non-existent table."""
    service = TableService(table_dao)
    result = service.get_table_capacity(999)

    assert result is None

# ---- Edge Cases ----
def test_min_capacity_table(table_dao, db_session):
    """Test handling minimum capacity table."""
    min_table = Table(capacity=1, location="Downtown")
    db_session.add(min_table)
    db_session.commit()
    service = TableService(table_dao)

    result = service.get_table_capacity(min_table.id)
    assert result == 1

def test_large_capacity_table(table_dao, db_session):
    """Test handling large capacity tables."""
    large_table = Table(capacity=12, location="Downtown")
    db_session.add(large_table)
    db_session.commit()
    service = TableService(table_dao)

    result = service.get_table_capacity(large_table.id)
    assert result == 12

# ---- Data Validation Tests ----
def test_empty_tables_list(table_dao):
    """Test when no tables exist in the database."""
    service = TableService(table_dao)
    result = service.get_all_tables()

    assert len(result) == 0  # Database starts empty for this test
