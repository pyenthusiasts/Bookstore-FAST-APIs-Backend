"""
Author management endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_active_user
from app.crud.author import (
    get_author_by_id,
    get_authors,
    create_author,
    update_author,
    delete_author,
)
from app.schemas.author import AuthorCreate, AuthorUpdate, AuthorResponse, AuthorWithBooks
from app.models.user import User
from app.core.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/", response_model=List[AuthorResponse])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get list of authors with pagination.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session

    Returns:
        List of authors
    """
    logger.info(f"Fetching authors list (skip={skip}, limit={limit})")
    authors = get_authors(db, skip=skip, limit=limit)
    return authors


@router.get("/{author_id}", response_model=AuthorWithBooks)
def read_author(author_id: int, db: Session = Depends(get_db)):
    """
    Get author by ID with their books.

    Args:
        author_id: Author ID
        db: Database session

    Returns:
        Author details with books

    Raises:
        HTTPException: If author not found
    """
    logger.info(f"Fetching author ID: {author_id}")
    db_author = get_author_by_id(db, author_id=author_id)
    if db_author is None:
        logger.warning(f"Author ID {author_id} not found")
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@router.post("/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
def create_author_endpoint(
    author: AuthorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new author (requires authentication).

    Args:
        author: Author creation data
        db: Database session
        current_user: Current authenticated user

    Returns:
        Created author
    """
    logger.info(f"User {current_user.username} creating author: {author.name}")
    db_author = create_author(db, author)
    logger.info(f"Author created successfully: {db_author.name} (ID: {db_author.id})")
    return db_author


@router.put("/{author_id}", response_model=AuthorResponse)
def update_author_endpoint(
    author_id: int,
    author: AuthorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update an author (requires authentication).

    Args:
        author_id: Author ID
        author: Author update data
        db: Database session
        current_user: Current authenticated user

    Returns:
        Updated author

    Raises:
        HTTPException: If author not found
    """
    logger.info(f"User {current_user.username} updating author ID: {author_id}")
    db_author = update_author(db, author_id=author_id, author=author)
    if db_author is None:
        logger.warning(f"Author ID {author_id} not found for update")
        raise HTTPException(status_code=404, detail="Author not found")
    logger.info(f"Author updated successfully: {db_author.name} (ID: {db_author.id})")
    return db_author


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author_endpoint(
    author_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Delete an author (requires authentication).

    Args:
        author_id: Author ID
        db: Database session
        current_user: Current authenticated user

    Raises:
        HTTPException: If author not found
    """
    logger.info(f"User {current_user.username} deleting author ID: {author_id}")
    success = delete_author(db, author_id=author_id)
    if not success:
        logger.warning(f"Author ID {author_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Author not found")
    logger.info(f"Author deleted successfully (ID: {author_id})")
