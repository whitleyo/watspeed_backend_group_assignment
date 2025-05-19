from app.domain.order import Order, OrderItem
from app.domain.menu_item import MenuItem
from app.messages.requests.order_request_dto import OrderRequestDTO, ModifyOrderRequestDTO
from app.messages.responses.order_response_dto import OrderResponseDTO
from app.daos.order_dao import OrderDAO

def order_request_to_domain(dto: OrderRequestDTO, order_dao: OrderDAO) -> Order:
    """
    Converts an OrderRequestDTO into an Order domain object using DAO to validate menu items and quantity.
    """
    menu_item_ids = {item["menu_item_id"]: item["quantity"] for item in dto.items}
    menu_items = order_dao.get_menu_items_by_ids(list(menu_item_ids.keys()))

    # Validate requested menu items exist
    existing_ids = {item.id for item in menu_items}
    invalid_ids = [item_id for item_id in menu_item_ids.keys() if item_id not in existing_ids]

    if invalid_ids:
        raise ValueError(f"Invalid menu item IDs: {invalid_ids}")

    # Create Order instance first
    order = Order(customer_name=dto.customer_name)

    # Add menu items using the method instead of manual initialization
    order.add_menu_items(menu_item_ids)

    return order


def modify_order_dto_to_domain(dto: ModifyOrderRequestDTO, existing_order: Order, order_dao: OrderDAO) -> Order:
    """
    Updates an existing Order domain object based on ModifyOrderRequestDTO using DAO for validation and quantity.
    """
    menu_item_ids = {item["menu_item_id"]: item["quantity"] for item in dto.items}
    menu_items = order_dao.get_menu_items_by_ids(list(menu_item_ids.keys()))

    # Validate requested menu items exist
    existing_ids = {item.id for item in menu_items}
    invalid_ids = [item_id for item_id in menu_item_ids.keys() if item_id not in existing_ids]

    if invalid_ids:
        raise ValueError(f"Invalid menu item IDs: {invalid_ids}")

    # Update order items with validated data
    existing_order.add_menu_items(menu_item_ids)

    # Update order status
    existing_order.status = dto.status if dto.status else existing_order.status

    return existing_order


def order_to_response(order: Order, message="Order placed successfully") -> OrderResponseDTO:
    """
    Converts an Order domain object into an OrderResponseDTO.
    """
    return OrderResponseDTO(
        order_id=order.id,
        customer_name=order.customer_name,
        order_items=[
            {"menu_item_id": item.menu_item.id, "name": item.menu_item.name, "size": item.menu_item.size,
             "price": item.menu_item.price, "quantity": item.quantity}
            for item in order.order_items
        ],
        status=order.status,
        message=message
    )