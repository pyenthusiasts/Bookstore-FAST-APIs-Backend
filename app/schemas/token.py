"""
Token schemas for authentication.
"""

from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """Schema for JWT token response."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token payload data."""

    username: Optional[str] = None
