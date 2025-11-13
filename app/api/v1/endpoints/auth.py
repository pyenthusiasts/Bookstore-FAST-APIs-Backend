"""
Authentication endpoints.
"""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.config import settings
from app.core.logging_config import get_logger
from app.core.security import create_access_token
from app.crud.user import authenticate_user, create_user, get_user_by_username
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse

logger = get_logger(__name__)

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        user: User registration data
        db: Database session

    Returns:
        Created user

    Raises:
        HTTPException: If username already exists
    """
    logger.info(f"Attempting to register user: {user.username}")

    # Check if user already exists
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        logger.warning(f"Registration failed: username '{user.username}' already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Create new user
    new_user = create_user(db, user)
    logger.info(f"User registered successfully: {new_user.username} (ID: {new_user.id})")
    return new_user


@router.post("/token", response_model=Token)
def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Authenticate user and return access token.

    Args:
        db: Database session
        form_data: Login form data with username and password

    Returns:
        JWT access token

    Raises:
        HTTPException: If credentials are invalid
    """
    logger.info(f"Login attempt for user: {form_data.username}")

    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Login failed: invalid credentials for user '{form_data.username}'")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    logger.info(f"User logged in successfully: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}
