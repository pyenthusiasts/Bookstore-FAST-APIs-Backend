"""
Book management endpoints.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user, get_db
from app.core.logging_config import get_logger
from app.crud.author import get_author_by_id
from app.crud.book import (
    create_book,
    delete_book,
    get_book_by_id,
    get_books,
    get_books_by_author,
    update_book,
)
from app.models.user import User
from app.schemas.book import BookCreate, BookResponse, BookUpdate, BookWithAuthor

logger = get_logger(__name__)

router = APIRouter()


@router.get("/", response_model=List[BookResponse])
def read_books(
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = Query(None, description="Filter by author ID"),
    db: Session = Depends(get_db),
):
    """
    Get list of books with pagination and optional author filter.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        author_id: Optional author ID to filter books
        db: Database session

    Returns:
        List of books
    """
    if author_id is not None:
        logger.info(f"Fetching books by author ID {author_id} (skip={skip}, limit={limit})")
        books = get_books_by_author(db, author_id=author_id, skip=skip, limit=limit)
    else:
        logger.info(f"Fetching all books (skip={skip}, limit={limit})")
        books = get_books(db, skip=skip, limit=limit)
    return books


@router.get("/{book_id}", response_model=BookWithAuthor)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """
    Get book by ID with author details.

    Args:
        book_id: Book ID
        db: Database session

    Returns:
        Book details with author

    Raises:
        HTTPException: If book not found
    """
    logger.info(f"Fetching book ID: {book_id}")
    db_book = get_book_by_id(db, book_id=book_id)
    if db_book is None:
        logger.warning(f"Book ID {book_id} not found")
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book_endpoint(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new book (requires authentication).

    Args:
        book: Book creation data
        db: Database session
        current_user: Current authenticated user

    Returns:
        Created book

    Raises:
        HTTPException: If author not found
    """
    logger.info(f"User {current_user.username} creating book: {book.title}")

    # Validate that author exists
    author = get_author_by_id(db, author_id=book.author_id)
    if author is None:
        logger.warning(f"Author ID {book.author_id} not found")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Author with ID {book.author_id} not found",
        )

    db_book = create_book(db, book)
    logger.info(f"Book created successfully: {db_book.title} (ID: {db_book.id})")
    return db_book


@router.put("/{book_id}", response_model=BookResponse)
def update_book_endpoint(
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update a book (requires authentication).

    Args:
        book_id: Book ID
        book: Book update data
        db: Database session
        current_user: Current authenticated user

    Returns:
        Updated book

    Raises:
        HTTPException: If book or author not found
    """
    logger.info(f"User {current_user.username} updating book ID: {book_id}")

    # Validate that author exists if author_id is being updated
    if book.author_id is not None:
        author = get_author_by_id(db, author_id=book.author_id)
        if author is None:
            logger.warning(f"Author ID {book.author_id} not found")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Author with ID {book.author_id} not found",
            )

    db_book = update_book(db, book_id=book_id, book=book)
    if db_book is None:
        logger.warning(f"Book ID {book_id} not found for update")
        raise HTTPException(status_code=404, detail="Book not found")

    logger.info(f"Book updated successfully: {db_book.title} (ID: {db_book.id})")
    return db_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book_endpoint(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Delete a book (requires authentication).

    Args:
        book_id: Book ID
        db: Database session
        current_user: Current authenticated user

    Raises:
        HTTPException: If book not found
    """
    logger.info(f"User {current_user.username} deleting book ID: {book_id}")
    success = delete_book(db, book_id=book_id)
    if not success:
        logger.warning(f"Book ID {book_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Book not found")
    logger.info(f"Book deleted successfully (ID: {book_id})")
