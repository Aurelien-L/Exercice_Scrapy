# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=list[schemas.Book])
def get_all_books(db: Session = Depends(get_db)):   
    """
    Returns a list of all books in the database
    """
    return crud.get_books(db)


@router.get("/{upc}", response_model=schemas.Book)
def get_book_by_upc(upc: str, db: Session = Depends(get_db)):
    """
    Returns a single book by its UPC.
    """
    db_book = crud.get_book_by_upc(db, upc)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.get("/search/", response_model=list[schemas.Book])
def get_books_by_title(title: str, db: Session = Depends(get_db)):
    """
    Returns a list of books with the given title.
    """
    books = crud.get_books_by_title(db, title)
    if not books:
        raise HTTPException(status_code=404, detail="No books found with that title")
    return books


@router.get("/category/{category_name}", response_model=list[schemas.Book])
def books_by_category(category_name: str, db: Session = Depends(get_db)):
    """
    Returns a list of books in the given category.
    """
    books = crud.get_books_by_category(db, category_name)
    if not books:
        raise HTTPException(status_code=404, detail="No books found in this category")
    return books


@router.get("/stock/below/{threshold}", response_model=list[schemas.Book])
def books_below_stock(threshold: int, db: Session = Depends(get_db)):
    """
    Returns a list of books that have a stock count below the given threshold.
    """
    return crud.get_books_below_stock(db, threshold)


@router.get("/rating/{min_rating}", response_model=list[schemas.Book])
def books_by_rating(min_rating: int, db: Session = Depends(get_db)):
    """
    Returns a list of books that have a rating greater than or equal to the given minimum rating.
    """
    return crud.get_books_by_rating(db, min_rating)


@router.get("/stock/in", response_model=list[schemas.Book])
def books_in_stock(db: Session = Depends(get_db)):
    """
    Returns a list of books that are currently in stock.
    """
    return crud.get_books_in_stock(db)


@router.get("/stock/out", response_model=list[schemas.Book])
def books_out_of_stock(db: Session = Depends(get_db)):
    """
    Returns a list of books that are currently out of stock.
    """
    return crud.get_books_out_of_stock(db)
