from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
SQLALCHEMY_DATABASE_URL =  os.getenv("DB_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Yield a database session object using a context manager.

    This function creates a database session object using the
    SessionLocal class from sqlalchemy.orm. The session object
    is then yielded using a context manager, which ensures that
    the session is properly closed after it is no longer needed.

    Yields:
        SessionLocal: A database session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
