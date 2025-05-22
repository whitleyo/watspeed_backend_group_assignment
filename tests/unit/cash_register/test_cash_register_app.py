import pytest
import json
from datetime import datetime
from cash_register.create_app import create_app  # Import the app factory function

@pytest.fixture
def client():
    """Creates a Flask test client from the application factory"""
    app = create_app()  # Create a new app instance
    app.testing = True  # Enable Flask test mode
    return app.test_client()

def test_missing_parameters(client):
    """Test request with missing parameters"""
    response = client.get("/transactions")
    assert response.status_code == 400
    assert "Missing required parameters" in response.get_json()["error"]

def test_invalid_date_format(client):
    """Test request with invalid date format"""
    response = client.get("/transactions?store_id=1&start_time=invalid&end_time=invalid")
    assert response.status_code == 400
    assert "Invalid date format" in response.get_json()["error"]

def test_start_time_after_end_time(client):
    """Test request where start_time is after end_time"""
    response = client.get("/transactions?store_id=1&start_time=2024-06-02T12:00:00&end_time=2024-06-01T10:00:00")
    assert response.status_code == 400
    assert "start_time must be before end_time" in response.get_json()["error"]

def test_valid_transaction_generation(client):
    """Test request with valid parameters"""
    response = client.get("/transactions?store_id=1&start_time=2024-06-01T10:00:00&end_time=2024-06-01T12:00:00")
    assert response.status_code == 200
    
    data = response.get_json()
    assert "transactions" in data
    assert isinstance(data["transactions"], list)
    
    for transaction in data["transactions"]:
        assert "time" in transaction
        try:
            # Ensure the time format is valid ISO 8601
            datetime.fromisoformat(transaction["time"])
        except ValueError:
            pytest.fail(f"Invalid time format: {transaction['time']}")
        assert "amount" in transaction
        assert 2 <= transaction["amount"] <= 20.0  # Amount should be in valid range

def test_transaction_time_within_range(client):
    """Ensure generated transactions fall within the requested time range"""
    start_time = "2024-06-01T10:00:00"
    end_time = "2024-06-01T12:00:00"
    
    response = client.get(f"/transactions?store_id=1&start_time={start_time}&end_time={end_time}")
    assert response.status_code == 200

    data = response.get_json()
    start_dt = datetime.fromisoformat(start_time)
    end_dt = datetime.fromisoformat(end_time)

    for transaction in data["transactions"]:
        transaction_time = datetime.fromisoformat(transaction["time"])
        assert start_dt <= transaction_time <= end_dt  # Ensure timestamp validity

