from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:deviabdd@localhost:5432/books"
SQLALCHEMY_DATABASE_URL =  os.getenv("DB_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()