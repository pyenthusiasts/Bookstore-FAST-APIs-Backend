"""
Schemas package.
"""

from app.schemas.author import AuthorCreate, AuthorResponse, AuthorUpdate, AuthorWithBooks
from app.schemas.book import BookCreate, BookResponse, BookUpdate, BookWithAuthor
from app.schemas.token import Token, TokenData
from app.schemas.user import UserCreate, UserInDB, UserResponse, UserUpdate

__all__ = [
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserInDB",
    "AuthorCreate",
    "AuthorUpdate",
    "AuthorResponse",
    "AuthorWithBooks",
    "BookCreate",
    "BookUpdate",
    "BookResponse",
    "BookWithAuthor",
    "Token",
    "TokenData",
]
