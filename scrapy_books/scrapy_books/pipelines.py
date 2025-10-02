# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


class ScrapyBooksPipeline:
    def process_item(self, item, spider):
        """
        Process the item and return it, or raise an exception if
        the item should be dropped.
        """
        return item


class ConvertRatingPipeline:
    def process_item(self, item, spider):
        """
        Process the item and return it, or raise an exception if
        the item should be dropped.

        This pipeline takes the rating of the book and converts it to a
        numerical value. The rating is extracted from the item and the last
        word of the rating string is used as the key to get the numerical
        value from the rating_map dictionary. If the rating is not found in
        the dictionary, it defaults to 0.
        """
        rating_map = {"One":1, "Two":2, "Three":3, "Four":4, "Five":5}
        rating_word = item.get("rating", "").split()[-1]
        item["rating"] = rating_map.get(rating_word, 0)
        return item
    

class AvailabilityPipeline:
    def process_item(self, item, spider):
        """
        Process the item and return it, or raise an exception if
        the item should be dropped.

        This pipeline checks the availability of the book and updates the
        item accordingly. If the book is "In stock", it extracts the
        available stock count from the availability text and updates the
        item with the count.
        """
        availability_text = item.get("availability", "").strip()

        item["availability"] = "Out of stock"
        item["stock_count"] = 0

        if availability_text:
            if "In stock" in availability_text:
                item["availability"] = "In stock"

                match = re.search(r"\((\d+)\s+available\)", availability_text)
                if match:
                    item["stock_count"] = int(match.group(1))

        return item
    

class CleanTextPipeline:
    def process_item(self, item, spider):
        """
        Clean the description of the book by replacing multiple spaces with a single space and removing all non-ASCII characters.
        """
        desc = item.get("description", "")
        if desc:
            desc = re.sub(r'\s+', ' ', desc)
            desc = re.sub(r'[^\x20-\x7E]+', '', desc)
            item["description"] = desc.strip()
        return item
    

class SavingToPostgresPipeline(object):

    def __init__(self):
        """
        Initialize the pipeline by creating a connection to the PostgreSQL database.
        """
        self.create_connection()

    def create_connection(self):
        """
        Create a connection to the PostgreSQL database.
        The connection and cursor are stored as instance variables self.conn and self.cur respectively.
        """
        load_dotenv()

        try:
            self.conn = psycopg2.connect(
                host=os.getenv("HOST"),
                database=os.getenv("DBNAME"),
                user=os.getenv("USER"),
                password=os.getenv("PASSWORD"),
                port=os.getenv("PORT")
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            print(f"Error connecting to database: {str(e)}")
            raise e


    def process_item(self, item, spider):
        """
        Process the item and store it in the PostgreSQL database.
        """
        self.store_db(item)
        return item
    

    def store_db(self, item):
        """
        Store the item in the PostgreSQL database.

        The item is first inserted into the categories table, and then
        inserted into the books table. If the item already exists in
        either table, the existing item is updated with the new data.

        Finally, the item is inserted into the stocks table with the
        id of the book in the books table.
        """
        try:
            self.cur.execute("""
                INSERT INTO categories (name) VALUES (%s)
                ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
                RETURNING id
            """, (item['category'],))
            category_id = self.cur.fetchone()[0]

            description = item.get("description", "")
            self.cur.execute("""
                INSERT INTO books (upc, title, description, category_id, rating)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (upc) DO UPDATE SET
                    title = EXCLUDED.title,
                    description = EXCLUDED.description,
                    category_id = EXCLUDED.category_id,
                    rating = EXCLUDED.rating
                RETURNING id
            """,  (
                    item.get("upc", ""),
                    item.get("title", "Unknown"),
                    description,
                    category_id,
                    item.get("rating", 0)
                ))
            book_id = self.cur.fetchone()[0]

            self.cur.execute("""
                INSERT INTO stocks (book_id, price, availability, stock_count)
                VALUES (%s, %s, %s, %s)
            """, (
                book_id,
                item['price'],
                item['availability'],
                item['stock_count']
            ))

            self.conn.commit()
        
        except Exception as e:
            print(f"❌ Error saving item: {str(e)}")
            self.conn.rollback()

        return item
    

    def close_connection(self, spider):
        """
        Close the connection to the PostgreSQL database after the spider has finished its work.
        """
        self.cur.close()
        self.conn.close()
    