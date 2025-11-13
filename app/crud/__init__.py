"""
CRUD operations package.
"""
from app.crud.user import (
    get_user_by_id,
    get_user_by_username,
    get_users,
    create_user,
    update_user,
    delete_user,
    authenticate_user,
)
from app.crud.author import (
    get_author_by_id,
    get_authors,
    create_author,
    update_author,
    delete_author,
)
from app.crud.book import (
    get_book_by_id,
    get_books,
    get_books_by_author,
    create_book,
    update_book,
    delete_book,
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
