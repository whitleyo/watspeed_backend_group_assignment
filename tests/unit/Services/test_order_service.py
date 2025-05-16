import pytest
from sqlalchemy.orm import sessionmaker
from app.domain.base import Base
from app.domain.menu_item import MenuItem
from app.domain.order import Order
from app.Services.order_service import OrderService
from app.daos.order_dao import OrderDAO
from app.messages.responses.order_response_dto import OrderResponseDTO, DeleteOrderResponseDTO
from app.messages.requests.order_request_dto import OrderRequestDTO, ModifyOrderRequestDTO, DeleteOrderRequestDTO
from sqlalchemy import create_engine

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
    """Ensures clean database state (order-wise) before each test."""
    db_session.query(Order).delete()
    db_session.query(MenuItem).delete()
    db_session.commit()

@pytest.fixture
def sample_menu_item(db_session):
    """Creates and stores a sample menu item."""
    item = MenuItem(name="Espresso", description="Bold coffee", size="Medium", price=3.0)
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    return item  # Return for test access

@pytest.fixture
def sample_menu_item2(db_session):
    """Creates and stores another sample menu item."""
    item = MenuItem(name="Cappuccino", description="Smooth coffee blend", size="Large", price=4.0)
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    return item

@pytest.fixture
def order_dao(db_session):
    """Provides an OrderDAO instance using a real database session."""
    return OrderDAO(session=db_session)

@pytest.fixture
def order_service(order_dao):
    """Provides an instance of OrderService using the DAO fixture."""
    return OrderService(order_dao)

def test_find_order_success(db_session, order_service, sample_menu_item):
    """Test finding an existing order via find_order()"""
    order = Order(customer_name="John Doe", menu_items=[sample_menu_item], quantity=2)
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)

    response = order_service.find_order(order.id)

    assert response is not None
    assert response.order_id == order.id
    assert response.menu_items[0].menu_id == sample_menu_item.id  # Verify list handling
    assert response.message == "Order placed successfully"

def test_find_order_not_found(order_service):
    """Test finding a non-existent order"""
    response = order_service.find_order(999)
    assert response is None

def test_find_all_orders(db_session, order_service, sample_menu_item, sample_menu_item2):
    """Test retrieving all orders via find_all_orders()"""
    order1 = Order(customer_name="Alice", menu_items=[sample_menu_item], quantity=1)
    order2 = Order(customer_name="Bob", menu_items=[sample_menu_item2], quantity=1)

    db_session.add_all([order1, order2])
    db_session.commit()

    responses = order_service.find_all_orders()

    assert len(responses) == 2
    assert responses[0].customer_name == "Alice"
    assert responses[0].menu_items[0].menu_id == sample_menu_item.id
    assert responses[1].customer_name == "Bob"
    assert responses[1].menu_items[0].menu_id == sample_menu_item2.id

def test_save_order(order_service, sample_menu_item, sample_menu_item2):
    """Test creating a new order with multiple menu items via save_order()"""
    order_dto = OrderRequestDTO(customer_name="Charlie", menu_item_ids=[sample_menu_item.id, sample_menu_item2.id], quantity=2)
    response = order_service.save_order(order_dto)

    assert isinstance(response, OrderResponseDTO)
    assert response.order_id > 0
    assert response.customer_name == "Charlie"
    assert len(response.menu_items) == 2  # Ensure multiple menu items are saved correctly

def test_modify_order_success(db_session, order_service, sample_menu_item2):
    """Test modifying an existing order via modify_order()"""
    order = Order(customer_name="David", menu_items=[sample_menu_item2], quantity=3)
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)

    modify_dto = ModifyOrderRequestDTO(order_id=order.id, menu_item_ids=[sample_menu_item2.id], quantity=4, status="completed")
    modify_response = order_service.modify_order(modify_dto)

    assert modify_response is not None
    assert modify_response.order_id == order.id
    assert modify_response.status == "completed"
    assert len(modify_response.menu_items) == 1

def test_modify_order_not_found(order_service):
    """Test modifying a non-existent order"""
    modify_dto = ModifyOrderRequestDTO(order_id=999, menu_item_ids=[7], quantity=1, status="completed")
    response = order_service.modify_order(modify_dto)

    assert response is None

def test_delete_order_success(db_session, order_service, sample_menu_item):
    """Test deleting an order via delete_order()"""
    order = Order(customer_name="Eve", menu_items=[sample_menu_item], quantity=1)
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)

    delete_request_dto = DeleteOrderRequestDTO(order_id=order.id)
    delete_response_dto = order_service.delete_order(delete_request_dto)

    assert db_session.get(Order, order.id) is None  # Ensures deletion
    assert isinstance(delete_response_dto, DeleteOrderResponseDTO)
    assert delete_response_dto.status == 0

def test_delete_order_not_found(order_service):
    """Test deleting a non-existent order"""
    delete_request_dto = DeleteOrderRequestDTO(order_id=999)
    delete_response_dto = order_service.delete_order(delete_request_dto)
    assert isinstance(delete_response_dto, DeleteOrderResponseDTO)
    assert delete_response_dto.status == 1
