# Bookstore API Backend with FastAPI

A modern, production-ready RESTful API for managing a bookstore, built with FastAPI. This project demonstrates best practices in API development, including proper project structure, authentication, testing, and containerization.

## Features

- **Modern Stack**: Built with FastAPI, SQLAlchemy 2.0, and Pydantic v2
- **JWT Authentication**: Secure endpoints with JSON Web Tokens
- **Complete CRUD**: Full Create, Read, Update, Delete operations for books, authors, and users
- **RESTful Design**: Clean API design following REST principles
- **Database Migrations**: Alembic integration for database version control
- **Testing**: Comprehensive test suite with pytest
- **Docker Support**: Containerized application with Docker and docker-compose
- **Code Quality**: Pre-commit hooks, Black, and Ruff for code formatting and linting
- **API Documentation**: Auto-generated interactive docs with Swagger UI and ReDoc
- **Logging**: Structured logging for better debugging and monitoring
- **CORS Support**: Configurable CORS middleware
- **Environment Configuration**: Settings management with pydantic-settings

## Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/pyenthusiasts/Bookstore-FAST-APIs-Backend.git
cd Bookstore-FAST-APIs-Backend

# Start the application
docker-compose up -d

# Seed the database (optional)
docker-compose exec api python scripts/seed_database.py

# Access the API at http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

### Local Development

```bash
# Clone the repository
git clone https://github.com/pyenthusiasts/Bookstore-FAST-APIs-Backend.git
cd Bookstore-FAST-APIs-Backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run migrations
alembic upgrade head

# Seed the database (optional)
python scripts/seed_database.py

# Run the application
uvicorn app.main:app --reload

# Or use Make
make run
```

## Project Structure

```
Bookstore-FAST-APIs-Backend/
│
├── app/                          # Application package
│   ├── api/                      # API layer
│   │   ├── v1/                   # API version 1
│   │   │   ├── endpoints/        # API endpoints
│   │   │   │   ├── auth.py       # Authentication endpoints
│   │   │   │   ├── users.py      # User management endpoints
│   │   │   │   ├── authors.py    # Author endpoints
│   │   │   │   └── books.py      # Book endpoints
│   │   │   └── __init__.py       # API router configuration
│   │   └── dependencies.py       # Shared dependencies
│   │
│   ├── core/                     # Core functionality
│   │   ├── config.py             # Configuration settings
│   │   ├── security.py           # Security utilities
│   │   └── logging_config.py     # Logging configuration
│   │
│   ├── crud/                     # Database operations
│   │   ├── user.py               # User CRUD operations
│   │   ├── author.py             # Author CRUD operations
│   │   └── book.py               # Book CRUD operations
│   │
│   ├── db/                       # Database layer
│   │   └── database.py           # Database configuration
│   │
│   ├── models/                   # SQLAlchemy models
│   │   ├── user.py               # User model
│   │   ├── author.py             # Author model
│   │   └── book.py               # Book model
│   │
│   ├── schemas/                  # Pydantic schemas
│   │   ├── user.py               # User schemas
│   │   ├── author.py             # Author schemas
│   │   ├── book.py               # Book schemas
│   │   └── token.py              # Token schemas
│   │
│   └── main.py                   # Application entry point
│
├── alembic/                      # Database migrations
│   ├── versions/                 # Migration scripts
│   └── env.py                    # Alembic configuration
│
├── scripts/                      # Utility scripts
│   └── seed_database.py          # Database seeding script
│
├── tests/                        # Test suite
│   ├── conftest.py               # Test configuration
│   ├── test_api.py               # API tests
│   └── test_auth.py              # Authentication tests
│
├── .env.example                  # Example environment variables
├── .gitignore                    # Git ignore rules
├── .pre-commit-config.yaml       # Pre-commit hooks configuration
├── alembic.ini                   # Alembic configuration
├── docker-compose.yml            # Docker Compose configuration
├── Dockerfile                    # Docker image definition
├── Makefile                      # Development commands
├── pyproject.toml                # Python project configuration
├── pytest.ini                    # Pytest configuration
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## API Endpoints

All API endpoints are prefixed with `/api/v1`.

### Authentication

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/token` - Login and get access token

### Users

- `GET /api/v1/users/me` - Get current user information
- `GET /api/v1/users/` - Get all users (authenticated)
- `GET /api/v1/users/{user_id}` - Get user by ID (authenticated)
- `PUT /api/v1/users/{user_id}` - Update user (authenticated, own profile only)
- `DELETE /api/v1/users/{user_id}` - Delete user (authenticated, own profile only)

### Authors

- `GET /api/v1/authors/` - Get all authors
- `GET /api/v1/authors/{author_id}` - Get author by ID with books
- `POST /api/v1/authors/` - Create author (authenticated)
- `PUT /api/v1/authors/{author_id}` - Update author (authenticated)
- `DELETE /api/v1/authors/{author_id}` - Delete author (authenticated)

### Books

- `GET /api/v1/books/` - Get all books (with optional author filter)
- `GET /api/v1/books/{book_id}` - Get book by ID with author details
- `POST /api/v1/books/` - Create book (authenticated)
- `PUT /api/v1/books/{book_id}` - Update book (authenticated)
- `DELETE /api/v1/books/{book_id}` - Delete book (authenticated)

## Usage Examples

### Register and Login

```bash
# Register a new user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "password": "secretpass123"}'

# Login to get access token
curl -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=secretpass123"
```

### Create Author and Book

```bash
# Create an author (requires authentication)
curl -X POST http://localhost:8000/api/v1/authors/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "J.K. Rowling"}'

# Create a book (requires authentication)
curl -X POST http://localhost:8000/api/v1/books/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Harry Potter and the Philosopher'\''s Stone",
    "description": "A young wizard'\''s journey begins",
    "author_id": 1
  }'
```

### Get Data

```bash
# Get all books
curl http://localhost:8000/api/v1/books/

# Get books by specific author
curl http://localhost:8000/api/v1/books/?author_id=1

# Get author with all their books
curl http://localhost:8000/api/v1/authors/1
```

## Development

### Running Tests

```bash
# Run all tests
make test

# Or use pytest directly
pytest

# Run with coverage
pytest --cov=app
```

### Code Quality

```bash
# Format code
make format

# Run linters
make lint

# Install pre-commit hooks
make dev-install
```

### Database Migrations

```bash
# Create a new migration
make migrate-create

# Apply migrations
make migrate

# Or use alembic directly
alembic revision --autogenerate -m "Add new field"
alembic upgrade head
```

### Makefile Commands

```bash
make help          # Show all available commands
make install       # Install production dependencies
make dev-install   # Install development dependencies
make test          # Run tests
make lint          # Run linters
make format        # Format code
make clean         # Clean build artifacts
make run           # Run the application
make seed          # Seed the database
make docker-up     # Start docker containers
make docker-down   # Stop docker containers
make migrate       # Run database migrations
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Application
APP_NAME=Bookstore API
DEBUG=False

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
SQLALCHEMY_DATABASE_URL=sqlite:///./bookstore.db

# CORS
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Logging
LOG_LEVEL=INFO
```

## Testing Credentials

When you seed the database, the following test users are created:

- Username: `admin` / Password: `admin123`
- Username: `user1` / Password: `password123`
- Username: `user2` / Password: `password123`
- Username: `user3` / Password: `password123`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework for building APIs
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation using Python type hints

---

**Happy Coding!** If you have any questions or feedback, please open an issue on GitHub.
