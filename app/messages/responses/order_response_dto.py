from pydantic import BaseModel, Field

class OrderResponseDTO(BaseModel):
    """
    DTO for order responses.
    """
    order_id: int = Field(..., description="Order ID")
    status: str = Field(..., description="Order status")
    message: str = Field(..., description="Optional confirmation message")

class DeleteOrderResponseDTO(BaseModel):
    """
    DTO for delete order responses.
    """
    status: int = Field(..., description="Status code")
    message: str = Field(..., description="Confirmation message")
