import pytest
from flask import Flask
from app.Routes.orders import order_bp  # Ensure routes are properly imported
# from app.dao.order_dao import OrderDAO
# from app.services.order_service import OrderService
# from app.messages.requests.order_request_dto import OrderRequestDTO, ModifyOrderRequestDTO

@pytest.fixture
def app():
    """Creates a Flask test application"""
    app = Flask(__name__)
    app.register_blueprint(order_bp)
    app.testing = True
    return app

@pytest.fixture
def client(app):
    """Provides a Flask test client"""
    return app.test_client()

@pytest.mark.usefixtures("client")
class TestOrderRoutes:
    """Test class for Flask routes, using pytest fixtures for setup"""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        """Runs before each test to reset Flask state"""
        self.client = client

    def test_create_order(self):
        """Test creating a new order via POST /order"""
        response = self.client.post('/order', json={
            "user_id": 1,
            "items": ["espresso"],
            "size": "medium"
        })
        data = response.get_json()

        assert response.status_code == 200
        assert data["status"] == "pending"
        assert data["message"] == "Order saved successfully"

    def test_modify_order_success(self):
        """Test modifying an existing order via PUT /order/modify"""
        create_response = self.client.post('/order', json={
            "user_id": 1,
            "items": ["latte"],
            "size": "large"
        })
        order_id = create_response.get_json()["order_id"]

        modify_response = self.client.put('/order/modify', json={
            "order_id": order_id,
            "items": ["cappuccino"],
            "size": "small"
        })
        data = modify_response.get_json()

        assert modify_response.status_code == 200
        assert data["status"] == "pending"
        assert data["message"] == "Order modified successfully"

    def test_modify_order_not_found(self):
        """Test modifying a non-existent order"""
        modify_response = self.client.put('/order/modify', json={
            "order_id": 999,
            "items": ["latte"],
            "size": "small"
        })
        data = modify_response.get_json()

        assert modify_response.status_code == 404
        assert data["status"] == 1
        assert data["message"] == "Order not found"

    def test_cancel_order_success(self):
        """Test cancelling an existing order via DELETE /order/cancel/{order_id}"""
        create_response = self.client.post('/order', json={
            "user_id": 1,
            "items": ["americano"],
            "size": "small"
        })
        order_id = create_response.get_json()["order_id"]

        cancel_response = self.client.delete(f'/order/cancel/{order_id}')
        data = cancel_response.get_json()

        assert cancel_response.status_code == 200
        assert data["status"] == 0
        assert data["message"] == "Order deleted successfully"

    def test_cancel_order_not_found(self):
        """Test cancelling a non-existent order"""
        cancel_response = self.client.delete('/order/cancel/999')
        data = cancel_response.get_json()

        assert cancel_response.status_code == 404
        assert data["status"] == 1
        assert data["message"] == "Order not found"
