from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models


# BOOKS FUNCTIONS

def get_books(db: Session):
    """
    Returns a list of all books in the database.
    """
    return db.query(models.Book).all()


def get_book_by_upc(db: Session, upc: str):
    """
    Returns a single book matching the given UPC, or None if no book is found.
    """
    return db.query(models.Book).filter(models.Book.upc == upc).first()


def get_books_by_title(db: Session, title: str):
    """
    Returns a list of all books in the database whose title contains the given title.
    """
    return db.query(models.Book).filter(models.Book.title.ilike(f"%{title}%")).all()


def get_books_by_category(db: Session, category_name: str):        
    """
    Returns a list of all books in the database whose category matches the given category name.
    The search is case-insensitive and will match any books whose category name contains the given string.
    """
    return (
        db.query(models.Book)
        .join(models.Category)
        .filter(models.Category.name.ilike(category_name))
        .all()
    )


def get_books_below_stock(db: Session, threshold: int):
    """
    Returns a list of all books in the database whose stock count is below the given threshold.
    The search is case-insensitive and will match any books whose stock count is below the given threshold.
    """
    return (
        db.query(models.Book)
        .join(models.Stock)
        .filter(models.Stock.stock_count < threshold)
        .all()
    )


def get_books_by_rating(db: Session, min_rating: int):
    """
    Returns a list of all books in the database whose rating is greater than or equal to the given min_rating.
    """
    return db.query(models.Book).filter(models.Book.rating >= min_rating).all()


def get_books_in_stock(db: Session):
    """
    Returns a list of all books in the database whose stock count is greater than zero.
    The search is case-insensitive and will match any books whose stock count is greater than zero.
    """
    return (
        db.query(models.Book)
        .join(models.Stock)
        .filter(models.Stock.availability.ilike("in stock"))
        .all()
    )


def get_books_out_of_stock(db: Session):
    """
    Returns a list of all books in the database whose stock count is zero or lower.
    The search is case-insensitive and will match any books whose stock count is zero or lower.
    """
    return (
        db.query(models.Book)
        .join(models.Stock)
        .filter(models.Stock.availability.ilike("out of stock"))
        .all()
    )



# CATEGORIES FUNCTIONS

def get_categories(db: Session):
    """
    Returns a list of all categories in the database.
    """
    return db.query(models.Category).all()



# STATS FUNCTIONS

def get_average_price(db: Session):
    """
    Returns the average price of all books in the database.
    """
    return db.query(func.avg(models.Stock.price)).scalar()


def get_average_price_by_category(db: Session):
    """
    Returns a list of dictionaries containing the name of a category and the average price of all books in that category.
    The list is sorted by category name.
    """   
    return (
        db.query(models.Category.name, func.avg(models.Stock.price))
        .join(models.Book, models.Category.id == models.Book.category_id)
        .join(models.Stock, models.Book.id == models.Stock.book_id)
        .group_by(models.Category.name)
        .all()
    )


def get_total_books(db: Session):
    """
    Returns the total number of books in the database.
    """
    return db.query(func.count(models.Book.id)).scalar()


def get_books_count_by_category(db: Session):
    """
    Returns a list of dictionaries containing the name of a category and the count of all books in that category.
    The list is sorted by category name.
    """
    return (
        db.query(models.Category.name, func.count(models.Book.id))
        .join(models.Book, models.Category.id == models.Book.category_id)
        .group_by(models.Category.name)
        .all()
    )


def get_books_between_prices(db: Session, min_price: float, max_price: float):
    """
    Returns a list of all books in the database whose price is between the given min_price and max_price.
    The search is inclusive, meaning that books with a price equal to min_price or max_price will be included in the result.
    """
    return (
        db.query(models.Book, models.Stock.price)
        .join(models.Stock, models.Book.id == models.Stock.book_id)
        .filter(models.Stock.price.between(min_price, max_price))
        .all()
    )


def get_top_rated_books_by_category(db: Session, category_name: str, limit: int = 10):
    """
    Returns a list of the top rated books in the given category, sorted by rating in descending order.
    The list is limited to the given number of books.
    Raises a 404 error if no books are found for the given category.
    """
    return (
        db.query(models.Book)
        .join(models.Category, models.Book.category_id == models.Category.id)
        .filter(models.Category.name == category_name)
        .order_by(models.Book.rating.desc())
        .limit(limit)
        .all()
    )
