import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../app/Routes")))
from flask import Flask
from menu import menu_bp  

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app = Flask(__name__)
    app.register_blueprint(menu_bp)
    app.testing = True
    return app.test_client()

def test_get_menu(client):
    """Test the GET /menu/ endpoint."""
    response = client.get('/menu/')
    assert response.status_code == 200
    data = response.get_json()
    assert type(data["status"]) is int
    assert type(data["data"]) is str
    assert data["status"] == int(0)
    assert data["data"] == str("data")

def test_get_menu_invalid_url(client):
    """Test the GET /menu/ endpoint for invalid url"""
    response = client.get('/menu/asdf')
    assert response.status_code == 404