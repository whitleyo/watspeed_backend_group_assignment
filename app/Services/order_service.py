from typing import Optional, List
from app.mappers.order_mapper import order_request_to_domain, modify_order_dto_to_domain, order_to_response
from app.messages.responses.order_response_dto import OrderResponseDTO, DeleteOrderResponseDTO
from app.messages.requests.order_request_dto import OrderRequestDTO, ModifyOrderRequestDTO, DeleteOrderRequestDTO
from app.daos.order_dao import OrderDAO
from app.domain.menu_item import MenuItem

class OrderService:
    def __init__(self, dao: OrderDAO):
        self.dao = dao

    def find_order(self, order_id: int) -> Optional[OrderResponseDTO]:
        """
        Find order by ID.
        """
        order = self.dao.find(order_id)
        return order_to_response(order) if order else None

    def find_all_orders(self) -> List[Optional[OrderResponseDTO]]:
        """
        Retrieve all orders.
        """
        orders = self.dao.findAll()
        return [order_to_response(order) for order in orders]

    def save_order(self, order_dto: OrderRequestDTO) -> OrderResponseDTO:
        """
        Save a new order with multiple menu items.
        """
        # Fetch menu items based on provided IDs
        menu_items = self.dao.find_menu_items(order_dto.menu_item_ids)
        
        if not menu_items:
            raise ValueError("Invalid menu item IDs provided")

        # Create order with multiple menu items
        order = order_request_to_domain(order_dto, menu_items)
        saved_order = self.dao.save(order)
        return order_to_response(saved_order, "Order saved successfully")

    def modify_order(self, modify_dto: ModifyOrderRequestDTO) -> Optional[OrderResponseDTO]:
        """
        Modify an existing order, updating its menu items.
        """
        existing_order = self.dao.find(modify_dto.order_id)
        if not existing_order:
            return None

        # Fetch updated menu items
        updated_menu_items = self.dao.find_menu_items(modify_dto.menu_item_ids)

        if not updated_menu_items:
            raise ValueError("Invalid menu item IDs provided")

        updated_order = modify_order_dto_to_domain(modify_dto, existing_order, updated_menu_items)
        saved_order = self.dao.update(updated_order.id, updated_order)
        return order_to_response(saved_order, "Order modified successfully")

    def delete_order(self, delete_dto: DeleteOrderRequestDTO) -> DeleteOrderResponseDTO:
        """
        Delete an existing order.
        """
        success = self.dao.delete(delete_dto.order_id)
        return DeleteOrderResponseDTO(
            status=0 if success else 1,
            message="Order deleted successfully" if success else "Order not found"
        )