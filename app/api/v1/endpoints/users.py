"""
User management endpoints.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user, get_db
from app.core.logging_config import get_logger
from app.crud.user import delete_user, get_user_by_id, get_users, update_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate

logger = get_logger(__name__)

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current user information.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user details
    """
    logger.info(f"User {current_user.username} retrieved their profile")
    return current_user


@router.get("/", response_model=List[UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get list of users (requires authentication).

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user: Current authenticated user

    Returns:
        List of users
    """
    logger.info(f"User {current_user.username} requested user list (skip={skip}, limit={limit})")
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get user by ID.

    Args:
        user_id: User ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        User details

    Raises:
        HTTPException: If user not found
    """
    logger.info(f"User {current_user.username} requested details for user ID: {user_id}")
    db_user = get_user_by_id(db, user_id=user_id)
    if db_user is None:
        logger.warning(f"User ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user_endpoint(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update user information.

    Args:
        user_id: User ID
        user: User update data
        db: Database session
        current_user: Current authenticated user

    Returns:
        Updated user

    Raises:
        HTTPException: If user not found or unauthorized
    """
    # Users can only update their own profile
    if current_user.id != user_id:
        logger.warning(
            f"User {current_user.username} attempted to update user ID {user_id} (unauthorized)"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user",
        )

    logger.info(f"User {current_user.username} updating their profile")
    db_user = update_user(db, user_id=user_id, user=user)
    if db_user is None:
        logger.warning(f"User ID {user_id} not found for update")
        raise HTTPException(status_code=404, detail="User not found")

    logger.info(f"User {current_user.username} profile updated successfully")
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Delete a user.

    Args:
        user_id: User ID
        db: Database session
        current_user: Current authenticated user

    Raises:
        HTTPException: If user not found or unauthorized
    """
    # Users can only delete their own account
    if current_user.id != user_id:
        logger.warning(
            f"User {current_user.username} attempted to delete user ID {user_id} (unauthorized)"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user",
        )

    logger.info(f"User {current_user.username} deleting their account")
    success = delete_user(db, user_id=user_id)
    if not success:
        logger.warning(f"User ID {user_id} not found for deletion")
        raise HTTPException(status_code=404, detail="User not found")

    logger.info(f"User account deleted successfully (ID: {user_id})")
