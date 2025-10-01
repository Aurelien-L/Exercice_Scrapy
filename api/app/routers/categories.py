from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[schemas.Category])
def list_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)
