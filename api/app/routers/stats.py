# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, database

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/average-price")
def average_price(db: Session = Depends(database.get_db)):
    """
    Returns the average price of all books in the database.
    """
    return {"average_price": crud.get_average_price(db)}


@router.get("/average-price/category")
def average_price_by_category(db: Session = Depends(database.get_db)):
    """
    Returns a list of objects containing the name of a category and the average price of all books in that category.
    The list is sorted by category name.
    """
    data = crud.get_average_price_by_category(db)
    return [{"category": name, "average_price": avg} for name, avg in data]


@router.get("/count/books")
def total_books(db: Session = Depends(database.get_db)):
    """
    Returns the total number of books in the database.
    """
    return {"total_books": crud.get_total_books(db)}


@router.get("/count/books/category")
def books_by_category(db: Session = Depends(database.get_db)):
    """
    Returns a list of objects containing the name of a category and the count of books in that category.
    The list is sorted by category name.
    """
    data = crud.get_books_count_by_category(db)
    return [{"category": name, "count": count} for name, count in data]


@router.get("/books/price-range")
def books_between_prices(min_price: float, max_price: float, db: Session = Depends(database.get_db)):
    """
    Returns a list of dictionaries containing the title and price of all books in the database 
    whose price is between the given min_price and max_price (inclusive).
    """
    results = crud.get_books_between_prices(db, min_price, max_price)
    return [{"title": b.title, "price": p} for b, p in results]


@router.get("/books/top-rated/{category_name}")
def top_rated_books(category_name: str, db: Session = Depends(database.get_db)):
    """
    Returns a list of dictionaries containing the title and rating of all books in the given category, sorted by rating in descending order.
    Raises a 404 error if no books are found for the given category.
    """
    results = crud.get_top_rated_books_by_category(db, category_name)
    if not results:
        raise HTTPException(status_code=404, detail="No books found for this category")
    return results
