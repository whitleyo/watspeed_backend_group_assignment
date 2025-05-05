import pytest
from app.domain.order import Order
from app.Services.order_service import OrderService
from app.daos.order_dao import OrderDAO
from app.messages.responses.order_response_dto import OrderResponseDTO, DeleteOrderResponseDTO
from app.messages.requests.order_request_dto import OrderRequestDTO, ModifyOrderRequestDTO, DeleteOrderRequestDTO
import app

@pytest.fixture
def order_dao():
    """Provides a simulated in-memory DAO instance"""
    return OrderDAO()

@pytest.fixture
def order_service(order_dao):
    """Provides an instance of OrderService using the DAO fixture"""
    return OrderService(order_dao)

@pytest.mark.usefixtures("order_dao", "order_service")
class TestOrderService:
    """Test class for OrderService, using pytest fixtures for setup"""

    @pytest.fixture(autouse=True)
    def setup(self, order_dao, order_service):
        """Runs before each test to reset state"""
        self.dao = order_dao
        self.service = order_service
        self.dao.orders.clear()

    def test_find_order_success(self):
        """Test finding an existing order via find_order()"""
        order_dto = OrderRequestDTO(user_id=1, items=["espresso"], size="medium")
        created_order = self.service.save_order(order_dto)

        response = self.service.find_order(created_order.order_id)

        assert response is not None
        assert response.order_id == created_order.order_id
        assert response.status == "pending"

    def test_find_order_not_found(self):
        """Test finding a non-existent order"""
        response = self.service.find_order(999)
        assert response is None

    def test_find_all_orders(self):
        """Test retrieving all orders via find_all_orders()"""
        order_dto1 = OrderRequestDTO(user_id=1, items=["americano"], size="small")
        order_dto2 = OrderRequestDTO(user_id=2, items=["cappuccino"], size="medium")

        created_order1 = self.service.save_order(order_dto1)
        created_order2 = self.service.save_order(order_dto2)

        responses = self.service.find_all_orders()

        assert len(responses) == 2
        assert responses[0].order_id == created_order1.order_id
        assert responses[1].order_id == created_order2.order_id

    def test_save_order(self):
        """Test creating a new order via save_order()"""
        order_dto = OrderRequestDTO(user_id=3, items=["latte"], size="large")
        response = self.service.save_order(order_dto)

        assert isinstance(response, OrderResponseDTO)
        assert response.order_id > 0
        assert response.status == "pending"
        assert response.message == "Order saved successfully"

    def test_modify_order_success(self):
        """Test modifying an existing order via modify_order()"""
        order_dto = OrderRequestDTO(user_id=1, items=["espresso"], size="medium")
        created_order = self.service.save_order(order_dto)

        modify_dto = ModifyOrderRequestDTO(order_id=created_order.order_id, items=["cappuccino"], size="small")
        modify_response = self.service.modify_order(modify_dto)

        assert modify_response is not None
        assert modify_response.order_id == created_order.order_id
        assert modify_response.status == "pending"
        assert modify_response.message == "Order modified successfully"

    def test_modify_order_not_found(self):
        """Test modifying a non-existent order"""
        modify_dto = ModifyOrderRequestDTO(order_id=999, items=["latte"], size="small")
        response = self.service.modify_order(modify_dto)

        assert response is None

    def test_delete_order_success(self):
        """Test deleting an order via delete_order()"""
        order_dto = OrderRequestDTO(user_id=3, items=["mocha"], size="large")
        created_order_response = self.service.save_order(order_dto)
        delete_request_dto = DeleteOrderRequestDTO(order_id=created_order_response.order_id)
        delete_response_dto = self.service.delete_order(delete_request_dto)
        assert self.dao.find(created_order_response.order_id) is None  # Ensures deletion
        assert isinstance(delete_response_dto, DeleteOrderResponseDTO)
        assert delete_response_dto.status == 0
        assert delete_response_dto.message == "Order deleted successfully"

    def test_delete_order_not_found(self):
        """Test deleting a non-existent order"""
        delete_request_dto = DeleteOrderRequestDTO(order_id=999)
        delete_response_dto = self.service.delete_order(delete_request_dto)
        assert isinstance(delete_response_dto, DeleteOrderResponseDTO)
        assert delete_response_dto.status == 1
        assert delete_response_dto.message == "Order not found"

