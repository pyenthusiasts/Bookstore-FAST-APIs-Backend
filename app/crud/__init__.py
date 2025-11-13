"""
CRUD operations package.
"""

from app.crud.author import (
    create_author,
    delete_author,
    get_author_by_id,
    get_authors,
    update_author,
)
from app.crud.book import (
    create_book,
    delete_book,
    get_book_by_id,
    get_books,
    get_books_by_author,
    update_book,
)
from app.crud.user import (
    authenticate_user,
    create_user,
    delete_user,
    get_user_by_id,
    get_user_by_username,
    get_users,
    update_user,
)

__all__ = [
    # User CRUD
    "get_user_by_id",
    "get_user_by_username",
    "get_users",
    "create_user",
    "update_user",
    "delete_user",
    "authenticate_user",
    # Author CRUD
    "get_author_by_id",
    "get_authors",
    "create_author",
    "update_author",
    "delete_author",
    # Book CRUD
    "get_book_by_id",
    "get_books",
    "get_books_by_author",
    "create_book",
    "update_book",
    "delete_book",
]
