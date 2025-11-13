"""
CRUD operations for authors.
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate


def get_author_by_id(db: Session, author_id: int) -> Optional[Author]:
    """
    Get an author by ID.

    Args:
        db: Database session
        author_id: Author ID

    Returns:
        Author or None if not found
    """
    return db.query(Author).filter(Author.id == author_id).first()


def get_authors(db: Session, skip: int = 0, limit: int = 100) -> list[Author]:
    """
    Get a list of authors with pagination.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of authors
    """
    return db.query(Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: AuthorCreate) -> Author:
    """
    Create a new author.

    Args:
        db: Database session
        author: Author creation schema

    Returns:
        Created author
    """
    db_author = Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(db: Session, author_id: int, author: AuthorUpdate) -> Optional[Author]:
    """
    Update an author.

    Args:
        db: Database session
        author_id: Author ID
        author: Author update schema

    Returns:
        Updated author or None if not found
    """
    db_author = get_author_by_id(db, author_id)
    if db_author is None:
        return None

    update_data = author.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_author, field, value)

    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int) -> bool:
    """
    Delete an author.

    Args:
        db: Database session
        author_id: Author ID

    Returns:
        True if deleted, False if not found
    """
    db_author = get_author_by_id(db, author_id)
    if db_author is None:
        return False

    db.delete(db_author)
    db.commit()
    return True
