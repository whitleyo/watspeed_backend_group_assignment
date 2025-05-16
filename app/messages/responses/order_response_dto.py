from pydantic import BaseModel, Field

class OrderResponseDTO(BaseModel):
    """
    DTO for order responses.
    """
    order_id: int = Field(..., description="Order ID")
    status: str = Field(..., description="Order status")
    customer_name: str = Field(..., description="Customer name")
    menu_id: int = Field(..., description="Menu ID")
    quantity: int = Field(..., description="Quantity of items ordered")
    order_time: str = Field(..., description="Order time in ISO format")
    message: str = Field(..., description="Optional confirmation message")

class DeleteOrderResponseDTO(BaseModel):
    """
    DTO for delete order responses.
    """
    status: int = Field(..., description="Status code")
    message: str = Field(..., description="Confirmation message")
