import pytest
from flask import Flask
from app.Routes.orders import order_bp  # Directly import the blueprint we're testing

@pytest.fixture
def app():
    """Create a minimal Flask app with ONLY the order blueprint"""
    app = Flask(__name__)
    app.config['TESTING'] = True
    
    # Register only the blueprint we're testing
    app.register_blueprint(order_bp)
    
    return app

@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()

def test_create_order(client):
    """Test order creation endpoint"""
    # Test with empty JSON since we're just testing the route
    response = client.post('/order', json={})
    assert response.status_code == 200
    assert response.json == {"status": 0, "data": "data"}

def test_modify_order(client):
    """Test order modification endpoint"""
    # Test with empty JSON and sample order ID
    response = client.put('/order/modify/1', json={})
    assert response.status_code == 200
    assert response.json == {"status": 0, "data": "data"}

def test_cancel_order(client):
    """Test order cancellation endpoint"""
    response = client.delete('/order/cancel/1')
    assert response.status_code == 200
    assert response.json == {"status": 0, "data": "data"}

def test_invalid_order_id(client):
    """Test invalid order ID format"""
    response = client.delete('/order/cancel/not_an_integer')
    assert response.status_code == 404
