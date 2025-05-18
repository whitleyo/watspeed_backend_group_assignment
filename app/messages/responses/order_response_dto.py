from pydantic import BaseModel, Field
from typing import List

class OrderResponseDTO(BaseModel):
    """
    DTO for order responses.
    """
    order_id: int = Field(..., description="Order ID")
    customer_name: str = Field(..., description="Customer name")
    order_items: List[dict] = Field(..., description="List of ordered menu items with quantity")
    status: str = Field(..., description="Order status")
    message: str = Field(..., description="Optional confirmation message")


class DeleteOrderResponseDTO(BaseModel):
    """
    DTO for delete order responses.
    """
    status: int = Field(..., description="Status code")
    message: str = Field(..., description="Confirmation message")
