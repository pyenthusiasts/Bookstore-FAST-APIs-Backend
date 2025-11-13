"""
User schemas for request/response validation.
"""

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    """Base user schema."""

    username: str = Field(..., min_length=3, max_length=50, description="Username")


class UserCreate(UserBase):
    """Schema for creating a user."""

    password: str = Field(..., min_length=6, description="Password")


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    username: str | None = Field(None, min_length=3, max_length=50)
    password: str | None = Field(None, min_length=6)
    is_active: bool | None = None


class UserResponse(UserBase):
    """Schema for user response."""

    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserResponse):
    """Schema for user in database."""

    hashed_password: str

    model_config = ConfigDict(from_attributes=True)
