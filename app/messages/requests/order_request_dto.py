from pydantic import BaseModel, Field
from typing import List

class OrderRequestDTO(BaseModel):
    """
    DTO for creating a new order.
    """
    menu_item_ids: List[int] = Field(..., description="List of Menu Item IDs")
    quantity: int = Field(..., description="Total quantity of items ordered")
    customer_name: str = Field(..., description="Customer name placing the order")

class ModifyOrderRequestDTO(BaseModel):
    """
    DTO for modifying an existing order.
    """
    order_id: int = Field(..., description="ID of the existing order")
    menu_item_ids: List[int] = Field(..., description="Updated list of Menu Item IDs")
    quantity: int = Field(..., description="Updated total quantity of items ordered")
    status: str = Field(..., description="Updated order status")

class DeleteOrderRequestDTO(BaseModel):
    """
    DTO for deleting an existing order.
    """
    order_id: int = Field(..., description="ID of the order to be deleted")