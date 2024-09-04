from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from datetime import timedelta

from database import engine, get_db
from models import Base
from schemas import UserCreate, UserResponse, BookCreate, BookResponse, AuthorCreate, AuthorResponse, Token
from crud import create_user, create_book, create_author, get_books, get_authors
from auth import create_access_token, get_current_user

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# User registration endpoint
@app.post("/users/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return db_user

# Authentication endpoint
@app.post("/token", response_model=Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Create a new book
@app.post("/books/", response_model=BookResponse)
def create_new_book(book: BookCreate, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return create_book(db, book)

# Get all books with pagination
@app.get("/books/", response_model=List[BookResponse])
def get_books_list(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_books(db, skip=skip, limit=limit)

# Create a new author
@app.post("/authors/", response_model=AuthorResponse)
def create_new_author(author: AuthorCreate, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return create_author(db, author)

# Get all authors with pagination
@app.get("/authors/", response_model=List[AuthorResponse])
def get_authors_list(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_authors(db, skip=skip, limit=limit)
