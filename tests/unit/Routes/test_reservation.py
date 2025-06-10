import pytest
import sys
import os
# Ensure correct module path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from flask import Flask, json
from unittest.mock import MagicMock
from app.Services.reservation_service import ReservationService
from app.domain.reservation import Reservation
from app.Routes.reservation import bp  # Import the blueprint dynamically
import app

class TestReservationRoutes:
    """Test class for reservation route endpoints."""

    @classmethod
    def setup_class(cls):
        """Set up Flask test client and mock dependency injection."""
        from app import create_app
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.mock_service = MagicMock(spec=ReservationService)

        # Override dependency injection globally for all tests
        def mock_binder(binder):
            binder.bind(ReservationService, to=cls.mock_service)

        from injector import Injector
        from flask_injector import FlaskInjector
        cls.injector = Injector([mock_binder])
        FlaskInjector(app=cls.app, injector=cls.injector)

    def test_create_reservation_success(self):
        """Test successful reservation creation."""
        self.mock_service.create_reservation.return_value = Reservation(10, "John Doe", 4, "2025-04-30T19:00:00")
        data = {"table_id": 10, "customer_name": "John Doe", "people_count": 4, "time": "2025-04-30T19:00:00"}
        
        res = self.client.post('/reservations/', json=data)

        assert res.status_code == 201
        assert res.json["table_id"] == 10
        assert res.json["customer_name"] == "John Doe"
        assert res.json["people_count"] == 4
        assert res.json["time"] == "2025-04-30T19:00:00"

    def test_get_reservation_success(self):
        """Test fetching an existing reservation."""
        self.mock_service.get_reservation.return_value = Reservation(10, "John Doe", 4, "2025-04-30T19:00:00")

        res = self.client.get('/reservations/1')

        assert res.status_code == 200
        assert res.json["customer_name"] == "John Doe"

    def test_get_reservation_not_found(self):
        """Test fetching a non-existent reservation."""
        self.mock_service.get_reservation.return_value = None

        res = self.client.get('/reservations/999')

        assert res.status_code == 404
        assert res.json == {"error": "Reservation not found"}

    def test_update_reservation_success(self):
        """Test updating a reservation."""
        self.mock_service.update_reservation.return_value = Reservation(10, "John Doe", 5, "2025-04-30T20:00:00")

        data = {"people_count": 5, "time": "2025-04-30T20:00:00"}
        res = self.client.put('/reservations/1', json=data)

        assert res.status_code == 200
        assert res.json["people_count"] == 5

    def test_cancel_reservation_success(self):
        """Test successful cancellation of a reservation."""
        self.mock_service.cancel_reservation.return_value = True

        res = self.client.delete('/reservations/1')

        assert res.status_code == 200
        assert res.json == {"message": "Reservation canceled"}

    def test_cancel_reservation_not_found(self):
        """Test canceling a non-existent reservation."""
        self.mock_service.cancel_reservation.return_value = False

        res = self.client.delete('/reservations/999')

        assert res.status_code == 404
        assert res.json == {"error": "Reservation not found"}