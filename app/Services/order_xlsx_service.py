from typing import Optional, List
from app.mappers.order_mapper import order_request_to_domain, modify_order_dto_to_domain, order_to_response
from app.messages.responses.order_response_dto import OrderResponseDTO, DeleteOrderResponseDTO
from app.messages.requests.order_request_dto import OrderRequestDTO, ModifyOrderRequestDTO, DeleteOrderRequestDTO
from app.daos.order_dao import OrderDAO

# NOTE: in reality we could just put the xlsx export functionality in the OrderService,
# but for the sake of separation of concerns, we are creating a separate service for it.

class OrderXLSXService:
    """Service for managing orders with XLSX export capabilities."""
    def __init__(self, order_dao: OrderDAO):
        self.dao = order_dao

    def find_all_orders(self) -> List[OrderResponseDTO]:
        """Find all orders."""
        raise NotImplementedError("TODO: implment XLSX export functionality")
        orders = self.dao.findAll()
        return [order_to_response(order) for order in orders]
            