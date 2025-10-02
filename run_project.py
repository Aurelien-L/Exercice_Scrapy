# -*- coding: utf-8 -*-
import sys
import os
import psycopg2
import subprocess
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

# Encoding Configuration
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

# Loading environment variables
load_dotenv()

# Importing templates after configuration
from api.app.database import Base


def create_database():
    """
    Create the PostgreSQL database if it doesn't already exist.

    This function connects to the PostgreSQL server using the environment variables,
    checks if the database already exists, and creates it if it doesn't.
    If the database already exists, it prints a success message.
    If an error occurs during the creation of the database, it prints an error message.
    """
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT")
        )
        
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (os.getenv("DBNAME"),))
        exists = cur.fetchone()

        if not exists:
            print(f"📚 Creation of the '{os.getenv('DBNAME')}' database...")
            cur.execute(f"CREATE DATABASE {os.getenv('DBNAME')}")
        else:
            print(f"✅ The '{os.getenv('DBNAME')}' database already exists.")

        cur.close()
        conn.close()

    except Exception as e:
        print("❌Error creating the database :", str(e))


def create_tables():
    """
    Create the tables in the PostgreSQL database if they don't already exist.

    This function connects to the PostgreSQL server using the environment variables,
    checks if the tables already exist, and creates them if they don't.
    If the tables already exist, it prints a success message.
    If an error occurs during the creation of the tables, it prints an error message.
    """
    try:
        from api.app.models import Book, Category
        
        engine = create_engine(
            f"postgresql://{os.getenv('USER')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DBNAME')}",
            echo=True
        )
        
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        print(f"Tables existantes avant création : {existing_tables}")
        
        Base.metadata.create_all(bind=engine)
        
        inspector = inspect(engine)
        tables_after = inspector.get_table_names()
        print(f"Tables après création : {tables_after}")
        
        print("✅ Tables created successfully.")
    except Exception as e:
        print("❌ Error creating tables:", str(e))
        raise e


def run_scrapy():
    """
    Run the Scrapy book spider.

    This function runs the Scrapy book spider in a subprocess and captures the output.
    If the spider runs successfully, it prints a success message.
    If the spider encounters an error, it prints an error message with the return code and output.
    """
    try:
        print("🔍 Launching scraping...")
        process = subprocess.run(
            ["scrapy", "crawl", "booksspider"],
            check=True,
            cwd=os.path.join(os.getcwd(), "scrapy_books"),
            capture_output=True,
            text=True
        )
        
        if process.stdout:
            print("Scrapy output:", process.stdout)
        if process.stderr:
            print("Scrapy errors:", process.stderr)
            
        if process.returncode == 0:
            print("✅ Scraping completed successfully.")
        else:
            print(f"⚠️ Scraping ended with return code {process.returncode}")
                
    except subprocess.CalledProcessError as e:
        print("❌ Error while scraping:")
        print(f"Return code: {e.returncode}")
        print(f"Output: {e.output}")
        print(f"Error output: {e.stderr}")
    except Exception as e:
        print("❌ Error while scraping:", str(e))


def run_fastpi():
    """
    Try to start the FastAPI API using Uvicorn.

    If successful, it will print a success message.
    If an error occurs, it will print an error message with the error details.
    """
    try:
        print("🚀 Starting the FastAPI API...")
        subprocess.run(["uvicorn", "api.app.main:app", "--reload"])
    except Exception as e:
        print("❌ Error while starting FastAPI:", e)


if __name__ == "__main__":
    print("=== Project launch ===")
    create_database()
    create_tables()
    run_scrapy()
    run_fastpi()
