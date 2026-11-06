from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book Library API",
    description="A simple API for managing books",
    version="2.0.0",
)


class BookCreate(BaseModel):
    title: str
    author: str
    year: int


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None


# ایجاد و بستن اتصال دیتابیس برای هر درخواست
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Welcome to the Book Library API"}


@app.get("/books")
def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()


@app.post("/books", status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = models.Book(
        title=book.title,
        author=book.author,
        year=book.year,
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


@app.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = (
        db.query(models.Book)
        .filter(models.Book.id == book_id)
        .first()
    )

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.patch("/books/{book_id}")
def update_book(
    book_id: int,
    book_update: BookUpdate,
    db: Session = Depends(get_db),
):
    book = (
        db.query(models.Book)
        .filter(models.Book.id == book_id)
        .first()
    )

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = book_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if value is not None:
            setattr(book, key, value)

    db.commit()
    db.refresh(book)

    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = (
        db.query(models.Book)
        .filter(models.Book.id == book_id)
        .first()
    )

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()

    return {
        "message": "Book deleted successfully",
        "book": book,
    }
