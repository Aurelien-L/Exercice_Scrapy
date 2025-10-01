from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routers import books, categories, stats


app = FastAPI(title="Scraped books API", version="1.0.0")

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

app.include_router(books.router)
app.include_router(categories.router)
app.include_router(stats.router)
