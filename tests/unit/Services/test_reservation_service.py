import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from app.domain.reservation import Reservation
from app.Services.reservation_service import ReservationService
from app.daos.reservation_dao import ReservationDAO
from app.daos.table_dao import TableDAO

class TestReservationService:
    @pytest.fixture
    def mock_daos(self):
        """Create mock DAOs for testing"""
        reservation_dao = MagicMock(spec=ReservationDAO)
        table_dao = MagicMock(spec=TableDAO)
        return reservation_dao, table_dao

    @pytest.fixture
    def sample_reservation(self):
        """Sample reservation fixture"""
        return Reservation(
            table_id=2,
            customer_name="Test Customer",
            people_count=4,
            time=(datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        )

    # ---- Creation Tests ----
    def test_create_reservation_success(self, mock_daos, sample_reservation):
        """Test successful reservation creation"""
        reservation_dao, table_dao = mock_daos
        table_dao.find.return_value = MagicMock(capacity=4)
        reservation_dao.save.return_value = sample_reservation
        
        service = ReservationService(reservation_dao, table_dao)
        result = service.create_reservation(
            table_id=2,
            customer_name="Test Customer",
            people_count=4,
            time="2023-12-01 14:00:00"
        )
        
        assert result == sample_reservation
        reservation_dao.save.assert_called_once()

    def test_create_reservation_table_not_found(self, mock_daos):
        """Test reservation with non-existent table"""
        reservation_dao, table_dao = mock_daos
        table_dao.find.return_value = None
        
        service = ReservationService(reservation_dao, table_dao)
        result = service.create_reservation(
            table_id=99,
            customer_name="Test Customer",
            people_count=4,
            time="2023-12-01 14:00:00"
        )
        
        assert result is None
        table_dao.find.assert_called_once_with(99)

    def test_create_reservation_exceeds_capacity(self, mock_daos):
        """Test reservation exceeding table capacity"""
        reservation_dao, table_dao = mock_daos
        table_dao.find.return_value = MagicMock(capacity=2)  # Table only fits 2
        
        service = ReservationService(reservation_dao, table_dao)
        result = service.create_reservation(
            table_id=1,
            customer_name="Test Customer",
            people_count=4,  # Trying to fit 4
            time="2023-12-01 14:00:00"
        )
        
        assert result is None
        table_dao.find.assert_called_once_with(1)

    # ---- Time Conflict Tests ----
    def test_create_reservation_time_conflict(self, mock_daos, sample_reservation):
        """Test reservation with conflicting time"""
        reservation_dao, table_dao = mock_daos
        table_dao.find.return_value = MagicMock(capacity=4)
        reservation_dao.find_by_table.return_value = [sample_reservation]  # Existing reservation
        
        service = ReservationService(reservation_dao, table_dao)
        result = service.create_reservation(
            table_id=2,
            customer_name="New Customer",
            people_count=4,
            time=sample_reservation.time  # Same time as existing
        )
        
        assert result is None
        reservation_dao.find_by_table.assert_called_once_with(2)

    # ---- Update Tests ----
    def test_update_reservation_success(self, mock_daos, sample_reservation):
        """Test successful reservation update"""
        reservation_dao, table_dao = mock_daos
        reservation_dao.find.return_value = sample_reservation
        table_dao.find.return_value = MagicMock(capacity=4)
        
        updated_reservation = Reservation(
            table_id=3,  # Changed table
            customer_name="Updated Customer",
            people_count=2,
            time="2023-12-01 15:00:00"
        )
        reservation_dao.save.return_value = updated_reservation
        
        service = ReservationService(reservation_dao, table_dao)
        result = service.update_reservation(
            reservation_id=1,
            table_id=3,
            customer_name="Updated Customer",
            people_count=2,
            time="2023-12-01 15:00:00"
        )
        
        assert result == updated_reservation
        reservation_dao.save.assert_called_once()

    def test_update_non_existent_reservation(self, mock_daos):
        """Test updating non-existent reservation"""
        reservation_dao, table_dao = mock_daos
        reservation_dao.find.return_value = None
        
        service = ReservationService(reservation_dao, table_dao)
        result = service.update_reservation(
            reservation_id=99,
            table_id=1,
            time="2023-12-01 14:00:00"
        )
        
        assert result is None
        reservation_dao.find.assert_called_once_with(99)

    # ---- Cancellation Tests ----
    def test_cancel_reservation_success(self, mock_daos):
        """Test successful cancellation"""
        reservation_dao, table_dao = mock_daos
        reservation_dao.delete.return_value = True
        
        service = ReservationService(reservation_dao, table_dao)
        result = service.cancel_reservation(1)
        
        assert result is True
        reservation_dao.delete.assert_called_once_with(1)

    def test_cancel_non_existent_reservation(self, mock_daos):
        """Test cancelling non-existent reservation"""
        reservation_dao, table_dao = mock_daos
        reservation_dao.delete.return_value = False
        
        service = ReservationService(reservation_dao, table_dao)
        result = service.cancel_reservation(99)
        
        assert result is False
        reservation_dao.delete.assert_called_once_with(99)

    # ---- Availability Tests ----
    def test_get_available_tables(self, mock_daos):
        """Test getting available tables"""
        reservation_dao, table_dao = mock_daos
        table_dao.findAll.return_value = [
            MagicMock(id=1, capacity=4),
            MagicMock(id=2, capacity=4),
            MagicMock(id=3, capacity=6)
        ]
        reservation_dao.findAll.return_value = [
            MagicMock(table_id=1, time="2023-12-01 14:00:00")
        ]
        
        service = ReservationService(reservation_dao, table_dao)
        result = service.get_available_tables("2023-12-01 14:00:00", 4)
        
        assert len(result) == 2  # Should exclude table 1 which is reserved
        assert all(t['capacity'] >= 4 for t in result)
        assert all(t['id'] in [2, 3] for t in result)

    def test_get_available_tables_no_reservations(self, mock_daos):
        """Test availability when no reservations exist"""
        reservation_dao, table_dao = mock_daos
        table_dao.findAll.return_value = [
            MagicMock(id=1, capacity=4),
            MagicMock(id=2, capacity=4)
        ]
        reservation_dao.findAll.return_value = []  # No reservations
        
        service = ReservationService(reservation_dao, table_dao)
        result = service.get_available_tables("2023-12-01 14:00:00", 4)
        
        assert len(result) == 2  # All tables available

    # ---- Edge Cases ----

    def test_create_reservation_min_people(self, mock_daos):
        """Test reservation with minimum people count (1)"""
        reservation_dao, table_dao = mock_daos
        table_dao.find.return_value = MagicMock(capacity=4)
        reservation_dao.save.return_value = MagicMock(people_count=1)
        
        service = ReservationService(reservation_dao, table_dao)
        result = service.create_reservation(
            table_id=1,
            customer_name="Solo Customer",
            people_count=1,
            time="2023-12-01 14:00:00"
        )
        
        assert result is not None
        assert result.people_count == 1