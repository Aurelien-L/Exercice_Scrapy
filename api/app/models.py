from sqlalchemy import Column, Integer, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, unique=True, nullable=False)

    books = relationship("Book", back_populates="category")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    upc = Column(Text, unique=True, nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    rating = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="books")
    stock = relationship("Stock", back_populates="book", uselist=False)


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    price = Column(Numeric(6, 2))
    availability = Column(Text)
    stock_count = Column(Integer, default=0)

    book = relationship("Book", back_populates="stock")
    