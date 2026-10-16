
# Book Library API

A simple REST API for managing books, built with FastAPI.

## Features

- Get all books
- Add a new book
- Get a book by ID
- Update a book using PATCH
- Delete a book by ID
- Automatic request validation
- Interactive API documentation

## Requirements

- Python 3.10 or newer
- pip

## Installation

Clone this repository:

```bash
git clone https://github.com/AsadullahAli/book-library-api.git
cd book-library-api
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the API

```bash
python -m uvicorn main:app --reload
```

Open the interactive documentation:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | / | Welcome message |
| GET | /books | Get all books |
| POST | /books | Create a book |
| GET | /books/{book_id} | Get a book by ID |
| PATCH | /books/{book_id} | Update a book |
| DELETE | /books/{book_id} | Delete a book by ID |

## Example Request

```json
{
  "title": "The Alchemist",
  "author": "Paulo Coelho",
  "year": 1988
}
```

## Storage

Books are stored in memory and are lost when the application restarts.
No database is used.
