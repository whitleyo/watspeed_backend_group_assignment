from pydantic import BaseModel, Field

class MenuItemResponseDTO(BaseModel):
    """
    DTO for menu item responses.
    """
    id: int = Field(..., description="Menu item ID")
    name: str = Field(..., description="Item name")
    description: str = Field(..., description="Item description")
    size: str= Field(..., description="Item size")
    price: float = Field(..., description="price of the item")
