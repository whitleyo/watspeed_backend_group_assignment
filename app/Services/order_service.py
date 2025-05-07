from typing import Optional, List
from app.mappers.order_mapper import order_request_to_domain, modify_order_dto_to_domain, order_to_response
from app.messages.responses.order_response_dto import OrderResponseDTO, DeleteOrderResponseDTO
from app.messages.requests.order_request_dto import OrderRequestDTO, ModifyOrderRequestDTO, DeleteOrderRequestDTO
from app.daos.order_dao import OrderDAO

class OrderService:
    def __init__(self, dao: OrderDAO):
        self.dao = dao

    def find_order(self, order_id: int) -> Optional[OrderResponseDTO]:
        """
        find order by id
        Args:
            order_id (int): The ID of the order to find.
        Returns:
            Optional[OrderResponseDTO]: The order response data transfer object if found, otherwise None.
        """
        order = self.dao.find(order_id)
        return order_to_response(order) if order else None

    def find_all_orders(self) -> List[Optional[OrderResponseDTO]]:
        """
        find all orders
        Returns:
            List[Optional[OrderResponseDTO]]: A list of order response data transfer objects containing all orders.
        """
        orders = self.dao.findAll()
        return [order_to_response(order) for order in orders]

    def save_order(self, order_dto: OrderRequestDTO) -> OrderResponseDTO:
        """
        save a new order
        Args:
            order_dto (OrderRequestDTO): The order data transfer object containing order details.
        Returns:
            OrderResponseDTO: The order response data transfer object containing the saved order details.
        """
        # effectively just creates a new order
        order = order_request_to_domain(order_dto)
        saved_order = self.dao.save(order)
        return order_to_response(saved_order, "Order saved successfully")

    def modify_order(self, modify_dto: ModifyOrderRequestDTO) -> Optional[OrderResponseDTO]:
        """
        Modify an existing order
        Args:
            modify_dto (ModifyOrderRequestDTO): The modify order data transfer object containing updated order details.
        Returns:
            Optional[OrderResponseDTO]: The order response data transfer object if the order was modified successfully, otherwise None.
        """
        existing_order = self.dao.find(modify_dto.order_id)
        if existing_order:
            updated_order = modify_order_dto_to_domain(modify_dto, existing_order)
            saved_order = self.dao.update(updated_order.id, updated_order)
            return order_to_response(saved_order, "Order modified successfully")
        return None

    def delete_order(self, delete_dto: DeleteOrderRequestDTO) -> DeleteOrderResponseDTO:
        """
        Delete an existing order
        Args:
            delete_dto (DeleteOrderRequestDTO): The delete order data transfer object containing the order ID to be deleted.
        """
        success = self.dao.delete(delete_dto.order_id)
        if success:
            response = DeleteOrderResponseDTO(status=0, message="Order deleted successfully")
        else:
            response = DeleteOrderResponseDTO(status=1, message="Order not found")
        return response
            