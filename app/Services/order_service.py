from typing import Optional, List
from app.mappers.order_mapper import order_request_to_domain, modify_order_dto_to_domain, order_to_response
from app.messages.responses.order_response_dto import OrderResponseDTO, DeleteOrderResponseDTO
from app.messages.requests.order_request_dto import OrderRequestDTO, ModifyOrderRequestDTO, DeleteOrderRequestDTO
from app.daos.order_dao import OrderDAO

class OrderService:
    def __init__(self, dao: OrderDAO):
        self.dao = dao

    def find_order(self, order_id: int) -> Optional[OrderResponseDTO]:
        """Find order by ID."""
        order = self.dao.find(order_id)
        return order_to_response(order) if order else None

    def find_all_orders(self) -> List[OrderResponseDTO]:
        """Find all orders."""
        orders = self.dao.findAll()
        return [order_to_response(order) for order in orders]

    def save_order(self, order_dto: OrderRequestDTO) -> OrderResponseDTO:
        """Save a new order."""
        order = order_request_to_domain(order_dto, self.dao)  # Mapper now constructs full Order object
        saved_order = self.dao.save(order)  # Pass the full Order object directly
        return order_to_response(saved_order, "Order saved successfully")

    def modify_order(self, modify_dto: ModifyOrderRequestDTO) -> Optional[OrderResponseDTO]:
        """Modify an existing order."""
        existing_order = self.dao.find(modify_dto.order_id)
        if existing_order:
            updated_order = modify_order_dto_to_domain(modify_dto, existing_order, self.dao)  # Fully structured Order
            saved_order = self.dao.update(updated_order.id, updated_order)  # Pass entire object to DAO
            return order_to_response(saved_order, "Order modified successfully")
        return None

    def delete_order(self, delete_dto: DeleteOrderRequestDTO) -> DeleteOrderResponseDTO:
        """Delete an existing order."""
        order = self.dao.find(delete_dto.order_id)
        if order:
            self.dao.delete(order.id)
            return DeleteOrderResponseDTO(status=0, message="Order deleted successfully")
        return DeleteOrderResponseDTO(status=1, message="Order not found")
            