import pytest
from unittest.mock import patch, mock_open, MagicMock
from flask import Flask
from datetime import datetime, timedelta
from pathlib import Path
from injector import Binder, singleton
from flask_injector import FlaskInjector

from app.Services.order_xlsx_service import OrderXLSXService
from app.Routes.orders import bp as order_bp

@pytest.fixture
def mock_order_xlsx_service(tmp_path):
    """Create a mock OrderXLSXService that returns a fake file path."""
    mock_service = MagicMock(spec=OrderXLSXService)
    fake_file = tmp_path / "orders.xlsx"
    fake_file.write_bytes(b"dummy excel content")
    mock_service.export_orders_to_xlsx.return_value = str(fake_file)
    return mock_service

@pytest.fixture
def client(mock_order_xlsx_service):
    """Set up Flask app with Flask-Injector and mock OrderXLSXService."""
    app = Flask(__name__)
    app.register_blueprint(order_bp)
    app.testing = True

    def configure(binder: Binder):
        binder.bind(OrderXLSXService, to=mock_order_xlsx_service, scope=singleton)

    FlaskInjector(app=app, modules=[configure])

    with app.test_client() as client:
        yield client

def test_order_spreadsheet_download_success(client):
    """Test basic download without date filters."""
    with patch("builtins.open", mock_open(read_data=b"dummy excel content")):
        response = client.get("/order/order_spreadsheet")

    assert response.status_code == 200
    assert response.headers["Content-Disposition"].startswith("attachment;")
    assert response.content_type in [
        "application/octet-stream",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ]

def test_order_spreadsheet_with_date_filter(client):
    """Test download with begin and end datetime filters."""
    begin = (datetime.now() - timedelta(days=1)).isoformat()
    end = datetime.now().isoformat()

    with patch("builtins.open", mock_open(read_data=b"filtered data")):
        response = client.get(
            "/order/order_spreadsheet",
            query_string={"begin_datetime": begin, "end_datetime": end}
        )

    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == "attachment; filename=orders.xlsx"

def test_order_spreadsheet_invalid_dates(client, mock_order_xlsx_service):
    """Test handling of invalid date input causing service failure."""
    # Force the mock to raise an exception like datetime.fromisoformat would
    mock_order_xlsx_service.export_orders_to_xlsx.side_effect = ValueError("Invalid datetime")

    response = client.get(
        "/order/order_spreadsheet",
        query_string={"begin_datetime": "bad", "end_datetime": "worse"}
    )

    assert response.status_code == 500
    assert b"Error generating spreadsheet" in response.data
