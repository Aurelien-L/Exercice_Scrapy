from pydantic import BaseModel
from typing import Optional


# ----------------------
# Category Schemas
# ----------------------
class Category(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


# ----------------------
# Stock Schemas
# ----------------------
class Stock(BaseModel):
    id: int
    price: Optional[float] = None
    availability: Optional[str] = None
    stock_count: Optional[int] = 0

    class Config:
        orm_mode = True


# ----------------------
# Book Schemas
# ----------------------
class Book(BaseModel):
    id: int
    upc: str
    title: str
    description: Optional[str] = None
    rating: Optional[int] = None

    category: Optional[Category] = None
    stock: Optional[Stock] = None

    class Config:
        orm_mode = True