import pytest
from unittest.mock import MagicMock, patch
from app.domain.table import Table
from app.Services.table_service import TableService
from app.daos.table_dao import TableDAO

class TestTableService:
    @pytest.fixture
    def mock_dao(self):
        """Create mock TableDAO for testing"""
        return MagicMock(spec=TableDAO)

    @pytest.fixture
    def sample_tables(self):
        """Sample tables fixture"""
        return [
            Table(id=1, shop_id=1, capacity=4),
            Table(id=2, shop_id=1, capacity=4),
            Table(id=3, shop_id=2, capacity=6)
        ]

    # ---- Basic CRUD Tests ----
    def test_get_table_success(self, mock_dao, sample_tables):
        """Test successfully getting a table"""
        mock_dao.find.return_value = sample_tables[0]
        service = TableService(mock_dao)
        result = service.get_table(1)
        
        assert result.id == 1
        assert result.capacity == 4
        mock_dao.find.assert_called_once_with(1)

    def test_get_table_not_found(self, mock_dao):
        """Test getting non-existent table"""
        mock_dao.find.return_value = None
        service = TableService(mock_dao)
        result = service.get_table(99)
        
        assert result is None
        mock_dao.find.assert_called_once_with(99)

    def test_get_all_tables(self, mock_dao, sample_tables):
        """Test getting all tables"""
        mock_dao.findAll.return_value = sample_tables
        service = TableService(mock_dao)
        result = service.get_all_tables()
        
        assert len(result) == 3
        assert isinstance(result[0], Table)
        mock_dao.findAll.assert_called_once()

    # ---- Shop-Specific Tests ----
    def test_get_tables_by_shop(self, mock_dao, sample_tables):
        """Test getting tables for specific shop"""
        mock_dao.find_by_shop.return_value = sample_tables[:2]  # First 2 tables are shop_id=1
        service = TableService(mock_dao)
        result = service.get_tables_by_shop(1)
        
        assert len(result) == 2
        assert all(table.shop_id == 1 for table in result)
        mock_dao.find_by_shop.assert_called_once_with(1)

    def test_get_tables_by_nonexistent_shop(self, mock_dao):
        """Test getting tables for non-existent shop"""
        mock_dao.find_by_shop.return_value = []
        service = TableService(mock_dao)
        result = service.get_tables_by_shop(99)
        
        assert len(result) == 0
        mock_dao.find_by_shop.assert_called_once_with(99)

    # ---- Capacity Tests ----
    def test_get_table_capacity_success(self, mock_dao):
        """Test getting table capacity"""
        mock_table = Table(id=1, shop_id=1, capacity=4)
        mock_dao.find.return_value = mock_table
        service = TableService(mock_dao)
        result = service.get_table_capacity(1)
        
        assert result == 4
        mock_dao.find.assert_called_once_with(1)

    def test_get_table_capacity_not_found(self, mock_dao):
        """Test getting capacity for non-existent table"""
        mock_dao.find.return_value = None
        service = TableService(mock_dao)
        result = service.get_table_capacity(99)
        
        assert result is None
        mock_dao.find.assert_called_once_with(99)

    # ---- Edge Cases ----
    def test_min_capacity_table(self, mock_dao):
        """Test table with minimum capacity (1)"""
        mock_table = Table(id=1, shop_id=1, capacity=1)
        mock_dao.find.return_value = mock_table
        service = TableService(mock_dao)
        result = service.get_table_capacity(1)
        
        assert result == 1

    def test_large_capacity_table(self, mock_dao):
        """Test table with large capacity"""
        mock_table = Table(id=1, shop_id=1, capacity=12)
        mock_dao.find.return_value = mock_table
        service = TableService(mock_dao)
        result = service.get_table_capacity(1)
        
        assert result == 12

    # ---- Data Validation Tests ----

    def test_empty_tables_list(self, mock_dao):
        """Test when no tables exist"""
        mock_dao.findAll.return_value = []
        service = TableService(mock_dao)
        result = service.get_all_tables()
        
        assert len(result) == 0
        mock_dao.findAll.assert_called_once()