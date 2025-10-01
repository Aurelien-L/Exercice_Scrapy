from fastapi import FastAPI
from app import models, database
from app.routers import books, categories


app = FastAPI(title="Scraped books API")

app.include_router(books.router)
app.include_router(categories.router)
