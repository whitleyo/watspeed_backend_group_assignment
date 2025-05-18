import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.domain.order import Order, OrderItem, Base
from app.Services.order_service import OrderService
from app.daos.order_dao import OrderDAO
from app.messages.responses.order_response_dto import OrderResponseDTO, DeleteOrderResponseDTO
from app.messages.requests.order_request_dto import OrderRequestDTO, ModifyOrderRequestDTO, DeleteOrderRequestDTO
from app.domain.menu_item import MenuItem
from typing import List

# Test database setup
TEST_DB_URL = "postgresql://test_user:test_password@localhost/test_db"
engine = create_engine(TEST_DB_URL)
Session = sessionmaker(bind=engine)

@pytest.fixture(scope="module")
def setup_database():
    """Sets up the test database before running tests."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def db_session(setup_database):
    """Provides a fresh database session for each test."""
    session = Session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture(autouse=True)
def clean_database(db_session):
    """Ensures clean database state before each test."""
    db_session.query(Order).delete()
    db_session.query(OrderItem).delete()
    db_session.query(MenuItem).delete()
    db_session.commit()

@pytest.fixture
def sample_menu_items(db_session):
    """Creates and stores multiple sample menu items."""
    items = [
        MenuItem(name="Espresso", description="Bold coffee", size="Medium", price=3.0),
        MenuItem(name="Cappuccino", description="Smooth coffee blend", size="Large", price=4.0)
    ]
    db_session.add_all(items)
    db_session.commit()
    [db_session.refresh(item) for item in items]
    return items

@pytest.fixture
def order_dao(db_session):
    """Provides an OrderDAO instance using a real database session."""
    return OrderDAO(db_session)

@pytest.fixture
def order_service(order_dao):
    """Provides an instance of OrderService using the DAO fixture."""
    return OrderService(order_dao)

@pytest.mark.usefixtures("order_dao", "order_service")
class TestOrderService:
    """Test class for OrderService, using pytest fixtures for setup."""

    @pytest.fixture(autouse=True)
    def setup(self, order_dao, order_service):
        """Runs before each test to reset state."""
        self.dao = order_dao
        self.service = order_service

    def test_find_order_success(self, db_session, sample_menu_items):
        """Test finding an existing order via find_order()."""
        order = Order(customer_name="John Doe")
        order.add_menu_items({item.id: 2 for item in sample_menu_items})  # Use add_menu_items

        db_session.add(order)
        db_session.commit()
        db_session.refresh(order)

        response = self.service.find_order(order.id)

        assert response is not None
        assert response.order_id == order.id
        assert len(response.order_items) == len(sample_menu_items)  # Validate multiple order items
        assert response.status == "pending"

    def test_find_order_not_found(self):
        """Test finding a non-existent order."""
        response = self.service.find_order(999)
        assert response is None

    def test_find_all_orders(self, db_session, sample_menu_items):
        """Test retrieving all orders via find_all_orders()."""
        order1 = Order(customer_name="Alice")
        order1.add_menu_items({sample_menu_items[0].id: 1})

        order2 = Order(customer_name="Bob")
        order2.add_menu_items({item.id: 2 for item in sample_menu_items})

        db_session.add_all([order1, order2])
        db_session.commit()

        responses = self.service.find_all_orders()

        assert len(responses) == 2
        assert len(responses[0].order_items) == 1
        assert len(responses[1].order_items) == 2

    def test_save_order(self, sample_menu_items):
        """Test creating a new order via save_order()."""
        order_dto = OrderRequestDTO(
            customer_name="Charlie",
            items=[{"menu_item_id": item.id, "quantity": 3} for item in sample_menu_items]
        )
        response = self.service.save_order(order_dto)

        assert isinstance(response, OrderResponseDTO)
        assert response.order_id > 0
        assert len(response.order_items) == len(sample_menu_items)  # Validate stored order items
        assert response.status == "pending"
        assert response.message == "Order saved successfully"

    def test_modify_order_success(self, db_session, sample_menu_items):
        """Test modifying an existing order via modify_order()."""
        order = Order(customer_name="David")
        order.add_menu_items({sample_menu_items[0].id: 2})
        
        db_session.add(order)
        db_session.commit()
        db_session.refresh(order)

        modify_dto = ModifyOrderRequestDTO(
            order_id=order.id,
            items=[{"menu_item_id": item.id, "quantity": 4} for item in sample_menu_items]
        )
        modify_response = self.service.modify_order(modify_dto)
        # manually checking table
        assert len(db_session.query(OrderItem).filter(OrderItem.order_id == order.id).all()) == len(sample_menu_items)  # Validate updated order items
        # other tests
        assert modify_response is not None
        assert modify_response.order_id == order.id
        assert len(modify_response.order_items) == len(sample_menu_items)  # Validate updated order items
        assert modify_response.status == "pending"
        assert modify_response.message == "Order modified successfully"

    def test_delete_order_success(self, db_session, sample_menu_items):
        """Test deleting an order via delete_order()."""
        order = Order(customer_name="Eve")
        order.add_menu_items({item.id: 1 for item in sample_menu_items})

        db_session.add(order)
        db_session.commit()
        db_session.refresh(order)

        delete_request_dto = DeleteOrderRequestDTO(order_id=order.id)
        delete_response_dto = self.service.delete_order(delete_request_dto)

        assert db_session.get(Order, order.id) is None  # Ensures deletion
        assert isinstance(delete_response_dto, DeleteOrderResponseDTO)
        assert delete_response_dto.status == 0
        assert delete_response_dto.message == "Order deleted successfully"
    def test_delete_order_not_found(self, db_session):
        """Test deleting a non-existent order."""
        delete_request_dto = DeleteOrderRequestDTO(order_id=999)
        delete_response_dto = self.service.delete_order(delete_request_dto)

        assert isinstance(delete_response_dto, DeleteOrderResponseDTO)
        assert delete_response_dto.status == 1
        assert delete_response_dto.message == "Order not found"

