from pydantic import BaseModel, Field
from typing import Optional

class UserRegistrationResponseDto(BaseModel):
    """DTO for creating a new user."""
    success: bool = Field(..., description="Registration result")
    message: str = Field(..., description="Confirmation or error message")
    user_id: Optional[int] = Field(description="User ID of the newly created user")

class UserLoginResponseDto(BaseModel):
    """DTO for creating a new user."""
    success: bool = Field(..., description="Login result")
    message: str = Field(..., description="Confirmation or error message")
    user_id: Optional[int] = Field(description="User ID of the logged in user")

class UseLogoutResponseDto(BaseModel):
    """DTO for creating a new user."""
    success: bool = Field(..., description="Logout result")
    message: str = Field(..., description="Confirmation or error message")
