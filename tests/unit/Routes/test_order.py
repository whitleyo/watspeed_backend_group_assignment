import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from flask import Flask

from app.Routes.orders import order_bp # Adjusted import path dynamically

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app = Flask(__name__)
    app.register_blueprint(order_bp)
    app.testing = True
    return app.test_client()

def test_create_order(client):
    """Test order creation with valid input"""
    new_order = {
        "customer_id": 123,
        "items": [{"item_id": 1, "quantity": 2}],
        "total_price": 25.50
    }
    response = client.post("/order", json=new_order)
    
    assert response.status_code == 201  # Expect created response
    data = response.json
    assert data["status"] == 0  # Assuming status 0 means success
    assert "order_id" in data["data"]  # Ensure order ID exists
    assert data["data"]["customer_id"] == 123  # Validate correct customer

def test_modify_order_valid(client):
    """Test modifying an existing order"""
    modified_order = {"items": [{"item_id": 2, "quantity": 3}]}
    response = client.put("/order/modify/1", json=modified_order)
    
    assert response.status_code == 200  # Expect success
    data = response.json
    assert "status" in data  # Check response structure
    assert data["status"] == 0  # Verify update was successful

def test_cancel_order(client):
    """Test order cancellation endpoint"""
    response = client.delete('/order/cancel/1')
    
    assert response.status_code == 200
    assert response.json == {"status": 0, "data": "Order 1 canceled"} 

def test_invalid_order_id(client):
    """Test invalid order ID format"""
    response = client.delete('/order/cancel/not_an_integer')
    assert response.status_code == 404

def test_create_order_invalid_data(client):
    """Test order creation with missing or invalid fields"""
    incomplete_order = {"customer_id": 123}  # Missing `items` and `total_price`
    response = client.post("/order", json=incomplete_order)

    assert response.status_code == 400  # Expect Bad Request

def test_cancel_order_not_found(client):
    """Test canceling an order that doesn't exist"""
    response = client.delete("/order/cancel/999999")  # Assume this ID doesn’t exist
    assert response.status_code == 404
