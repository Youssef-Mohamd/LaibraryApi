

# Library Management System API

A RESTful API built with FastAPI for managing a library's book inventory and tracking book borrowing operations.

---

## 📚 Features

- **Book Management**: Add, retrieve, update, and delete books
- **Inventory Tracking**: Monitor available copies of each book
- **Borrowing System**: Handle book checkouts and returns
- **Standardized Responses**: Consistent API response format across all endpoints

---

##  Prerequisites

- Python 3.7+
- pip (Python package installer)

---

##  Installation

1. Clone the repository or download the source code

2. Install required dependencies:

```bash
pip install fastapi pydantic uvicorn
```

---

##  Running the Application

Start the server using uvicorn:

```bash
uvicorn main:server --reload
```

The API will be available at `http://localhost:8000`

### Interactive API Documentation

You can test all API endpoints using Postman or any HTTP client by sending requests

- **Postman**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs

---

#  API Endpoints

### Health Check

#### `GET /`

Check if the API is running.

**Response:**

```json
{
  "health": "ok",
  "status": "success"
}
```

---

### Books

#### `GET /books`

Retrieve all books in the library.

**Response:**

```json
{
  "success": true,
  "message": "Books retrieved successfully",
  "data": {
    "books": [...]
  }
}
```

---

#### `GET /books/{book_id}`

Retrieve a specific book by its ID.

**Parameters:**

- `book_id` (path): The book's unique identifier

**Response:**

```json
{
  "success": true,
  "message": "Book retrieved successfully",
  "data": {
    "book": {
      "id": 1,
      "title": "Clean Code",
      "author": "Robert C. Martin",
      "available_copies": 4
    }
  }
}
```

---

#### `POST /books`

Add a new book to the library.

**Request Body:**

```json
{
  "id": 4,
  "title": "Refactoring",
  "author": "Martin Fowler",
  "available_copies": 5
}
```

**Response:**

```json
{
  "success": true,
  "message": "Book added successfully",
  "data": {
    "book": {...}
  }
}
```

---

#### `PUT /books/{book_id}`

Update an existing book's information.

**Parameters:**

- `book_id` (path): The book's unique identifier

**Request Body:**

```json
{
  "id": 1,
  "title": "Clean Code - Updated",
  "author": "Robert C. Martin",
  "available_copies": 5
}
```

---

#### `DELETE /books/{book_id}`

Remove a book from the library.

**Parameters:**

- `book_id` (path): The book's unique identifier

**Response:**

```json
{
  "success": true,
  "message": "Book deleted",
  "data": {
    "book": {...}
  }
}
```

---

### Borrowing Operations

#### `POST /borrow`

Borrow a book from the library.

**Request Body:**

```json
{
  "book_id": 1,
  "user_id": "user123"
}
```

**Response:**

```json
{
  "success": true,
  "message": "Book 'Clean Code' borrowed successfully",
  "data": {
    "available_copies": 3
  }
}
```

---

#### `POST /return`

Return a borrowed book to the library.

**Request Body:**

```json
{
  "book_id": 1,
  "user_id": "user123"
}
```

**Response:**

```json
{
  "success": true,
  "message": "Book 'Clean Code' returned successfully",
  "data": {
    "available_copies": 4
  }
}
```

---

## 📋 Data Models

### Book

```python
{
  "id": int,
  "title": str,
  "author": str,
  "available_copies": int
}
```

### BorrowRequest

```python
{
  "book_id": int,
  "user_id": str
}
```

### BorrowRecord

```python
{
  "book_id": int,
  "user_id": str,
  "book_title": str,
  "borrow_date": datetime
}
```

### StandardResponse

```python
{
  "success": bool,
  "message": str,
  "data": dict
}
```

---

## 📖 Sample Data

The API comes pre-populated with three books:

1. **Clean Code** by Robert C. Martin (4 copies)
2. **The Pragmatic Programmer** by Andrew Hunt (2 copies)
3. **Design Patterns** by Erich Gamma (3 copies)

---

## ⚠️ Error Handling

All endpoints return standardized error responses:

```json
{
  "success": false,
  "message": "Error description",
  "data": {}
}
```

### Common Error Scenarios

- Book not found
- Book with this ID already exists
- No copies available for borrowing
- Borrow record not found (when returning)

---

## 👨‍💻 Project By
- Youssef Mohamed Salem

