from pydantic import BaseModel
from typing import Optional

class Category(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}


class Stock(BaseModel):
    id: int
    price: Optional[float] = None
    availability: Optional[str] = None
    stock_count: Optional[int] = 0
    model_config = {"from_attributes": True}


class Book(BaseModel):
    id: int
    upc: str
    title: str
    description: Optional[str] = None
    rating: Optional[int] = None

    category: Optional[Category] = None
    stock: Optional[Stock] = None

    model_config = {"from_attributes": True}
    