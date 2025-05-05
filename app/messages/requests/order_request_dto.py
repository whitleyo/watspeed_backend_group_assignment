from pydantic import BaseModel, Field
from typing import List

class OrderRequestDTO(BaseModel):
    """
    DTO for creating a new order.
    """
    items: List[str] = Field(..., description="List of coffee item names")
    size: str = Field(..., description="Coffee size (e.g., Small, Medium, Large)")
    user_id: int = Field(..., description="ID of the user placing the order")


class ModifyOrderRequestDTO(BaseModel):
    """
    DTO for modifying an existing order.
    """
    order_id: int = Field(..., description="ID of the existing order")
    items: List[str] = Field(..., description="Updated list of coffee item names")
    size: str = Field(..., description="Updated coffee size (e.g., Small, Medium, Large)")

class DeleteOrderRequestDTO(BaseModel):
    """
    DTO for deleting an existing order.
    """
    order_id: int = Field(..., description="ID of the order to be deleted")
