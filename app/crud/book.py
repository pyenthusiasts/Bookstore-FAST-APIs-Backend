"""
CRUD operations for books.
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate


def get_book_by_id(db: Session, book_id: int) -> Optional[Book]:
    """
    Get a book by ID.

    Args:
        db: Database session
        book_id: Book ID

    Returns:
        Book or None if not found
    """
    return db.query(Book).filter(Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 100) -> list[Book]:
    """
    Get a list of books with pagination.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of books
    """
    return db.query(Book).offset(skip).limit(limit).all()


def get_books_by_author(db: Session, author_id: int, skip: int = 0, limit: int = 100) -> list[Book]:
    """
    Get books by author ID.

    Args:
        db: Database session
        author_id: Author ID
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of books by the author
    """
    return db.query(Book).filter(Book.author_id == author_id).offset(skip).limit(limit).all()


def create_book(db: Session, book: BookCreate) -> Book:
    """
    Create a new book.

    Args:
        db: Database session
        book: Book creation schema

    Returns:
        Created book
    """
    db_book = Book(title=book.title, description=book.description, author_id=book.author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book: BookUpdate) -> Optional[Book]:
    """
    Update a book.

    Args:
        db: Database session
        book_id: Book ID
        book: Book update schema

    Returns:
        Updated book or None if not found
    """
    db_book = get_book_by_id(db, book_id)
    if db_book is None:
        return None

    update_data = book.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> bool:
    """
    Delete a book.

    Args:
        db: Database session
        book_id: Book ID

    Returns:
        True if deleted, False if not found
    """
    db_book = get_book_by_id(db, book_id)
    if db_book is None:
        return False

    db.delete(db_book)
    db.commit()
    return True
