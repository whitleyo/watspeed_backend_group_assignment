from pydantic import BaseModel, Field

class ReservationResponseDTO(BaseModel):
    """
    DTO for reservation responses.
    """
    table_id: int = Field(..., description="Table ID")
    customer_name: str = Field(..., description="Name of the customer making the reservation")
    people_count: int = Field(..., description="Number of people for the reservation")
    time: str = Field(..., description="Time of the reservation (could be a datetime object)")
