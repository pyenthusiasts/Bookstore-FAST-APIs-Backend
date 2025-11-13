"""
Author schemas for request/response validation.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class AuthorBase(BaseModel):
    """Base author schema."""

    name: str = Field(..., min_length=1, max_length=100, description="Author name")


class AuthorCreate(AuthorBase):
    """Schema for creating an author."""

    pass


class AuthorUpdate(BaseModel):
    """Schema for updating an author."""

    name: str | None = Field(None, min_length=1, max_length=100)


class AuthorResponse(AuthorBase):
    """Schema for author response."""

    id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorWithBooks(AuthorResponse):
    """Schema for author response with books."""

    books: List["BookResponse"] = []

    model_config = ConfigDict(from_attributes=True)


# Import BookResponse for forward reference
from app.schemas.book import BookResponse

# Update forward references
AuthorWithBooks.model_rebuild()
