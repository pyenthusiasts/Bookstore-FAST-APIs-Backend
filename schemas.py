from pydantic import BaseModel
from typing import List, Optional

# User schemas
class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool

# JWT token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Book schemas
class BookCreate(BaseModel):
    title: str
    description: Optional[str] = None
    author_id: int

class BookResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    author_id: int

# Author schemas
class AuthorCreate(BaseModel):
    name: str

class AuthorResponse(BaseModel):
    id: int
    name: str
    books: List[BookResponse] = []
