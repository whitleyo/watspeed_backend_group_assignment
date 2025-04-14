import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../app/Routes")))
from flask import Flask

from orders import order_bp # Adjusted import path dynamically

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app = Flask(__name__)
    app.register_blueprint(order_bp)
    app.testing = True
    return app.test_client()

# Test data
TEST_ORDER_ID = 123

def test_cancel_order_route(client):
    """Test order cancellation endpoint"""
    response = client.delete(f'/order/cancel/{TEST_ORDER_ID}')
    assert response.status_code == 200
    assert response.json == {"status": 0, "data": "data"}

def test_create_order_route(client):
    """Test order creation endpoint"""
    response = client.post('/order', json={
        'items': [{'coffee_type': 'latte', 'size': 'medium'}]
    })
    assert response.status_code == 200
    assert response.json == {"status": 0, "data": "data"}

def test_modify_order_route(client):
    """Test order modification endpoint"""
    response = client.put(f'/order/modify/{TEST_ORDER_ID}', json={
        'new_items': [{'coffee_type': 'americano', 'size': 'large'}]
    })
    assert response.status_code == 200
    assert response.json == {"status": 0, "data": "data"}

def test_invalid_order_id(client):
    """Test non-integer order ID handling"""
    response = client.delete('/order/cancel/abc')
    assert response.status_code == 404

def test_missing_order_id(client):
    """Test missing order ID in URL"""
    response = client.delete('/order/cancel/')
    assert response.status_code == 404