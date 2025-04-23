from pydantic import BaseModel, EmailStr, Field

# Originally this was separated into two DTOs, one for login and one for registration
# but since they have the same fields, we can combine them into one
class UserRequestDto(BaseModel):
    """DTO for logging in or creating a new user."""
    username: str = Field(..., description="User name")
    email: EmailStr = Field(..., description="User email address")
