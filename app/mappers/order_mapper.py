from app.domain.order import Order
from app.messages.requests.order_request_dto import OrderRequestDTO, ModifyOrderRequestDTO
from app.messages.responses.order_response_dto import OrderResponseDTO


def order_request_to_domain(dto: OrderRequestDTO) -> Order:
    return Order(
        id=None,
        user_id=dto.user_id,
        items=dto.items,
        size=dto.size,
        status="pending",
        timestamp=""  # Should be added by service when created
    )


def modify_order_dto_to_domain(dto: ModifyOrderRequestDTO, existing_order: Order) -> Order:
    existing_order.items = dto.items
    existing_order.size = dto.size
    return existing_order


def order_to_response(order: Order, message="Order placed successfully") -> OrderResponseDTO:
    return OrderResponseDTO(
        order_id=order.id,
        status=order.status,
        message=message
    )
