import pytest
import sys
import os
from flask import Flask
# Adjust the path to import reservations_bp from ../../app/Routes/reservation.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../app/Routes")))
from reservation import reservations_bp, reserved_seats  # Adjusted import path dynamically

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app = Flask(__name__)
    app.register_blueprint(reservations_bp)
    app.testing = True
    return app.test_client()

def test_cancel_non_existent_id(client):
    """Test if cancellation of a non-existent id returns status 1 and 'data' as a string."""
    response = client.delete('/reservations/cancel-seat/99')  # ID 99 assumed to be non-existent
    data = response.get_json()
    assert response.status_code == 200  # Function returns JSON instead of 404
    assert data["status"] == 1
    assert data["data"] == "data"

def test_reserve_new_id(client):
    """Test if reservation of a new id returns status 0, 'data' as a string, and id exists in reserved_seats."""
    response = client.post('/reservations/reserve-seat/100')  # ID 100 assumed to be new
    data = response.get_json()
    assert response.status_code == 200  # Function returns JSON instead of 201
    assert data["status"] == 0
    assert data["data"] == "data"
    assert 100 in reserved_seats  # Ensure seat was added

def test_reserve_existing_id(client):
    """Test if reservation of an existing id returns status 1 and 'data' as a string."""
    client.post('/reservations/reserve-seat/101')  # Reserve ID first
    response = client.post('/reservations/reserve-seat/101')  # Try to reserve again
    data = response.get_json()
    assert response.status_code == 200  # Function returns JSON instead of 404
    assert data["status"] == 1
    assert data["data"] == "data"

def test_cancel_existing_id(client):
    """Test if cancellation of an existing id returns status 0, 'data' as a string, and id is removed."""
    client.post('/reservations/reserve-seat/102')  # Reserve ID first
    response = client.delete('/reservations/cancel-seat/102')  # Cancel it
    data = response.get_json()
    assert response.status_code == 200
    assert data["status"] == 0
    assert data["data"] == "data"
    assert 102 not in reserved_seats  # Ensure seat was removed