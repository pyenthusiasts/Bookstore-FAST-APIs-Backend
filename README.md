# Bookstore API Backend with FastAPI

This project demonstrates a sophisticated backend API for a **Bookstore** application, built using **FastAPI**, a modern, fast (high-performance) web framework for building APIs with Python. The API provides features for managing books and authors, including full CRUD operations, JWT-based authentication, database integration using SQLAlchemy, and pagination. It also includes automated seeding of the database with fake data for testing purposes.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Project Structure](#project-structure)
6. [API Endpoints](#api-endpoints)
7. [Examples](#examples)
8. [Contributing](#contributing)
9. [License](#license)

## Introduction

The Bookstore API provides a secure and scalable backend service for managing books and authors in a bookstore. It demonstrates key backend development concepts using FastAPI, such as asynchronous endpoints, JWT authentication, and database integration with SQLAlchemy. The API is designed to be easily extended and deployed, making it a great starting point for more complex applications.

## Features

- **JWT Authentication**: Secure API endpoints with JSON Web Tokens for authentication.
- **CRUD Operations**: Full Create, Read, Update, Delete operations for books and authors.
- **Database Integration**: Persistent storage using **SQLite** with SQLAlchemy ORM.
- **Async Endpoints**: Asynchronous endpoints for improved performance.
- **Pagination**: Efficient handling of large datasets with pagination.
- **Error Handling**: Graceful error handling with meaningful HTTP status codes and messages.
- **Modular Structure**: Organized codebase with multiple files for scalability and maintainability.
- **Automated Database Seeding**: Use of Faker library to generate and seed the database with fake data.

## Installation

### Prerequisites

- Python 3.7 or higher

### Install Required Packages

1. **Clone the Repository**:

   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/bookstore-api-fastapi.git
   ```

2. **Navigate to the Directory**:

   Go to the project directory:

   ```bash
   cd bookstore-api-fastapi
   ```

3. **Install Dependencies**:

   Install the required packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Application**:

   Start the FastAPI application using Uvicorn:

   ```bash
   uvicorn main:app --reload
   ```

   The server will start at `http://127.0.0.1:8000/`.

2. **Access API Documentation**:

   FastAPI provides interactive API documentation at:

   - **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Project Structure

```
bookstore/
│
├── main.py                # Entry point of the application
├── models.py              # SQLAlchemy models representing the database schema
├── schemas.py             # Pydantic models for request and response validation
├── crud.py                # CRUD operations for interacting with the database
├── auth.py                # Authentication logic (JWT token creation and verification)
├── database.py            # Database setup and session management
├── config.py              # Configuration settings (e.g., secrets, JWT settings)
├── seed_data.py           # Script for seeding the database with fake data
└── requirements.txt       # List of required Python packages
```

## API Endpoints

### 1. User Registration

- **Endpoint**: `POST /users/`
- **Description**: Register a new user.
- **Request Body**:
  ```json
  {
    "username": "user1",
    "password": "yourpassword"
  }
  ```
- **Response**: User details (excluding password).

### 2. User Authentication

- **Endpoint**: `POST /token`
- **Description**: Authenticate user and receive a JWT token.
- **Request Body**: Form data (`username`, `password`).
- **Response**: JWT token.

### 3. Create a New Book

- **Endpoint**: `POST /books/`
- **Description**: Add a new book (requires authentication).
- **Request Body**:
  ```json
  {
    "title": "The Great Gatsby",
    "description": "A novel by F. Scott Fitzgerald",
    "author_id": 1
  }
  ```
- **Response**: Book details.

### 4. Get All Books

- **Endpoint**: `GET /books/`
- **Description**: Retrieve all books with pagination.
- **Query Parameters**: `skip` (default: 0), `limit` (default: 10).
- **Response**: List of books.

### 5. Create a New Author

- **Endpoint**: `POST /authors/`
- **Description**: Add a new author (requires authentication).
- **Request Body**:
  ```json
  {
    "name": "F. Scott Fitzgerald"
  }
  ```
- **Response**: Author details.

### 6. Get All Authors

- **Endpoint**: `GET /authors/`
- **Description**: Retrieve all authors with pagination.
- **Query Parameters**: `skip` (default: 0), `limit` (default: 10).
- **Response**: List of authors.

## Examples

### Using cURL

1. **Register a New User**:

   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"username": "user1", "password": "yourpassword"}' http://127.0.0.1:8000/users/
   ```

2. **Authenticate and Get Token**:

   ```bash
   curl -X POST -d "username=user1&password=yourpassword" -H "Content-Type: application/x-www-form-urlencoded" http://127.0.0.1:8000/token
   ```

3. **Create a New Book**:

   ```bash
   curl -X POST -H "Authorization: Bearer <your-token>" -H "Content-Type: application/json" -d '{"title": "The Great Gatsby", "description": "A novel by F. Scott Fitzgerald", "author_id": 1}' http://127.0.0.1:8000/books/
   ```

4. **Get All Books**:

   ```bash
   curl -X GET http://127.0.0.1:8000/books/
   ```

## Contributing

Contributions are welcome! If you have ideas for new features, improvements, or bug fixes, please feel free to open an issue or create a pull request.

### Steps to Contribute

1. **Fork the Repository**: Click the 'Fork' button at the top right of this page.
2. **Clone Your Fork**: Clone your forked repository to your local machine.
   ```bash
   git clone https://github.com/your-username/bookstore-api-fastapi.git
   ```
3. **Create a Branch**: Create a new branch for your feature or bug fix.
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make Changes**: Make your changes and commit them with a descriptive message.
   ```bash
   git commit -m "Add: feature description"
   ```
5. **Push Changes**: Push your changes to your forked repository.
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Create a Pull Request**: Go to the original repository on GitHub and create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Thank you for using the Bookstore API Backend with FastAPI! If you have any questions or feedback, feel free to reach out to [me](mailto:hoangson091104@gmail.com). Happy coding! 📚🚀
