"""
API v1 router.
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, authors, books

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(authors.router, prefix="/authors", tags=["Authors"])
api_router.include_router(books.router, prefix="/books", tags=["Books"])
