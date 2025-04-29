from pydantic import BaseModel, Field
from typing import List, Dict

class MenuItemResponseDTO(BaseModel):
    """
    DTO for menu item responses.
    """
    id: int = Field(..., description="Menu item ID")
    name: str = Field(..., description="Item name")
    description: str = Field(..., description="Item description")
    sizes: List[str] = Field(..., description="Available sizes")
    prices: Dict[str, float] = Field(..., description="Mapping of size to price")
