from pydantic import BaseModel, Field
from typing import List

class OrderRequestDTO(BaseModel):
    """
    DTO for creating a new order.
    """
    customer_name: str = Field(..., description="Name of the customer placing the order")
    items: List[dict] = Field(..., description="List of menu items, each with menu_item_id and quantity")

class ModifyOrderRequestDTO(BaseModel):
    """
    DTO for modifying an existing order.
    """
    order_id: int = Field(..., description="ID of the existing order")
    items: List[dict] = Field(..., description="Updated list of menu items, each with menu_item_id and quantity")
    status: str = Field(None, description="Updated order status (optional)")



class DeleteOrderRequestDTO(BaseModel):
    """
    DTO for deleting an existing order.
    """
    order_id: int = Field(..., description="ID of the order to be deleted")
