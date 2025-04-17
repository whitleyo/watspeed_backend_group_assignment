import pytest
from flask import Flask
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app.Routes.auth import auth_bp

@pytest.fixture
def client():
    # Create a Flask app and register the auth blueprint
    app = Flask(__name__)
    app.register_blueprint(auth_bp)
    app.testing = True
    return app.test_client()

def test_register(client):
    # Simulate a POST request to the /register route
    response = client.post('/register', json={
        "username": "testuser",
        "password": "password123",
        "email": "testuser@example.com"
    })
    assert response.json["status"] == int(0)
    assert response.json["data"] == str("data")

def test_sign_in(client):
    # Simulate a POST request to the /sign-in route
    response = client.post('/sign-in', json={
        "username": "testuser",
        "password": "password123"
    })
    assert response.json["status"] == int(0)
    assert response.json["data"] == str("data")

def test_sign_out(client):
    # Simulate a POST request to the /sign-out route
    response = client.post('/sign-out')
    assert response.json["status"] == int(0)
    assert response.json["data"] == str("data")

# Unhappy path tests

def test_invalid_register(client):
    # Simulate an invalid POST request to the /register route
    response = client.post('/register', json={
        "username": "testuser",
        "password": 1234,
        "email": "testuser@example.com"
    })
    assert response.json["status"] == int(1)

def test_invalid_sign_in(client):
    # Simulate an invalid POST request to the /sign-in route
    response = client.post('/sign-in', json={})
    assert response.json["status"] == int(1)
