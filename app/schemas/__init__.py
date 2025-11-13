"""
Schemas package.
"""
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserInDB
from app.schemas.author import AuthorCreate, AuthorUpdate, AuthorResponse, AuthorWithBooks
from app.schemas.book import BookCreate, BookUpdate, BookResponse, BookWithAuthor
from app.schemas.token import Token, TokenData

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
