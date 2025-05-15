import pytest
from flask import Flask, json
from unittest.mock import MagicMock
from app.Services.table_service import TableService
from app.domain.table import Table
from app.Routes.table import bp  # Import the table routes
import app

class TestTableRoutes:
    """Test class for table route endpoints."""

    @classmethod
    def setup_class(cls):
        """Set up Flask test client and mock dependency injection."""
        from app import create_app
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.mock_service = MagicMock(spec=TableService)

        # Override dependency injection globally for all tests
        def mock_binder(binder):
            binder.bind(TableService, to=cls.mock_service)

        from injector import Injector
        from flask_injector import FlaskInjector
        cls.injector = Injector([mock_binder])
        FlaskInjector(app=cls.app, injector=cls.injector)

    def test_get_all_tables_success(self):
        """Test retrieving all tables."""
        self.mock_service.get_all_tables.return_value = [
            Table(capacity=4, location="Front Street"),
            Table(capacity=6, location="Front Street")
        ]

        res = self.client.get('/tables/')
        print(res.json)
        assert res.status_code == 200
        assert len(res.json) == 2
        assert res.json[0]["capacity"] == 4
        assert res.json[0]["location"] == "Front Street"

    def test_get_table_success(self):
        """Test retrieving a specific table."""
        self.mock_service.get_table.return_value = Table(capacity=6, location="Queen Street")

        res = self.client.get('/tables/2')
        assert res.status_code == 200
        assert res.json["capacity"] == 6
        assert res.json["location"] == "Queen Street"

    def test_get_table_not_found(self):
        """Test retrieving a table that doesn't exist."""
        self.mock_service.get_table.return_value = None

        res = self.client.get('/tables/999')
        print(res.json)
        assert res.status_code == 404
        assert res.json == {"error": "Table not found"}

    def test_get_shop_tables_success(self):
        """Test retrieving tables from a specific shop."""
        self.mock_service.get_tables_by_location.return_value = [
            Table(capacity=8, location="Front Street"),
            Table(capacity=6, location="Front Street")
        ]

        res = self.client.get('/tables/shop/Front Street')
        assert res.status_code == 200
        assert len(res.json) == 2
        assert res.json[0]["capacity"] == 8

    def test_get_shop_tables_empty(self):
        """Test retrieving tables for a shop with no tables."""
        self.mock_service.get_tables_by_location.return_value = []

        res = self.client.get('/tables/shop/999')
        assert res.status_code == 200
        assert res.json == []