"""
Book schemas for request/response validation.
"""

from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from app.schemas.author import AuthorResponse


class BookBase(BaseModel):
    """Base book schema."""

    title: str = Field(..., min_length=1, max_length=200, description="Book title")
    description: Optional[str] = Field(None, max_length=1000, description="Book description")


class BookCreate(BookBase):
    """Schema for creating a book."""

    author_id: int = Field(..., gt=0, description="Author ID")


class BookUpdate(BaseModel):
    """Schema for updating a book."""

    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    author_id: int | None = Field(None, gt=0)


class BookResponse(BookBase):
    """Schema for book response."""

    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)


class BookWithAuthor(BookResponse):
    """Schema for book response with author details."""

    author: "AuthorResponse"

    model_config = ConfigDict(from_attributes=True)
