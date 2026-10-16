
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Book Library API",
    description="A simple API for managing books",
    version="1.0.0",
)


class BookCreate(BaseModel):
    title: str
    author: str
    year: int


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None


books = []
next_id = 1


@app.get("/")
def home():
    return {"message": "Welcome to the Book Library API"}


@app.get("/books")
def get_books():
    return books


@app.post("/books", status_code=201)
def create_book(book: BookCreate):
    global next_id

    new_book = {
        "id": next_id,
        "title": book.title,
        "author": book.author,
        "year": book.year,
    }

    books.append(new_book)
    next_id += 1
    return new_book


@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=404, detail="Book not found")


@app.patch("/books/{book_id}")
def update_book(book_id: int, book_update: BookUpdate):
    for book in books:
        if book["id"] == book_id:
            update_data = book_update.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                if value is not None:
                    book[key] = value

            return book

    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            deleted_book = books.pop(index)
            return {
                "message": "Book deleted successfully",
                "book": deleted_book,
            }

    raise HTTPException(status_code=404, detail="Book not found")
