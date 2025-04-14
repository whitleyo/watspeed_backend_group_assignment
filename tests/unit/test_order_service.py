import pytest
import sys
import os
from flask import Flask
from pathlib import Path
from app.Routes.orders import order_bp
# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../app/Routes")))
from app import create_app  # Import your app factory

@pytest.fixture
def app():
    """Create and configure a test Flask app using your factory"""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create a test client"""
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