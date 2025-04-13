import pytest
from flask import Flask
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

    assert response.status_code == 200
    assert response.json["status"] == int(1)
    assert response.json["data"] == str("data")

def test_sign_in(client):
    # Simulate a POST request to the /sign-in route
    response = client.post('/sign-in', json={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 200
    assert response.json["status"] == int(1)
    assert response.json["data"] == str("data")

def test_sign_out(client):
    # Simulate a POST request to the /sign-out route
    response = client.post('/sign-out')
    assert response.status_code == 200
    assert response.json["status"] == int(1)
    assert response.json["data"] == str("data")
