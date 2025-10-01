from sqlalchemy.orm import Session
from . import models


def get_books(db: Session):
    return db.query(models.Book).all()


def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books_by_title(db: Session, title: str):
    return db.query(models.Book).filter(models.Book.title.ilike(f"%{title}%")).all()


def get_books_by_category(db: Session, category_name: str):
    return (
        db.query(models.Book)
        .join(models.Category)
        .filter(models.Category.name.ilike(category_name))
        .all()
    )


def get_categories(db: Session):
    return db.query(models.Category).all()


def get_books_below_stock(db: Session, threshold: int):
    return (
        db.query(models.Book)
        .join(models.Stock)
        .filter(models.Stock.stock_count < threshold)
        .all()
    )


def get_books_by_rating(db: Session, min_rating: int):
    return db.query(models.Book).filter(models.Book.rating >= min_rating).all()


def get_books_in_stock(db: Session):
    return (
        db.query(models.Book)
        .join(models.Stock)
        .filter(models.Stock.availability.ilike("in stock"))
        .all()
    )


def get_books_out_of_stock(db: Session):
    return (
        db.query(models.Book)
        .join(models.Stock)
        .filter(models.Stock.availability.ilike("out of stock"))
        .all()
    )