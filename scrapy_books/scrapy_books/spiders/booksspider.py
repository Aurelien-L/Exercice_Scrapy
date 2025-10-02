# -*- coding: utf-8 -*-

import scrapy
from scrapy_books.items import BooksInformations
from scrapy_books.itemloaders import BooksInformationsLoader
import os
from dotenv import load_dotenv

load_dotenv()


class BooksSpider(scrapy.Spider):
    name = "booksspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = [os.getenv("START_URL")]

    def parse(self, response):        
        """
        Parse the page and extract the book URLs, then yield the response.follow() of the book URLs.
        Also parse the next page URL and yield the response.follow() of the next page URL.
        """
        for book in response.css("article.product_pod"):
            relative_url = book.css("h3 a::attr(href)").get(default="")
            if relative_url:
                full_url = response.urljoin(relative_url)
                yield response.follow(full_url, callback=self.parse_book)

            yield response.follow(full_url, callback=self.parse_book)

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def parse_book(self, response):
        """
        Parse the book page and extract the book information.
        """
        
        loader = BooksInformationsLoader(item=BooksInformations(), selector=response)

        loader.add_css("title", "h1::text", default="Unknown Title")
        loader.add_css("price", ".price_color::text", default="0")
        loader.add_css("availability", ".instock.availability::text", default="")
        loader.add_css("description", "#product_description ~ p::text", default="")
        loader.add_css("category", ".breadcrumb li:nth-child(3) a::text", default="Unknown")
        loader.add_css("rating", "p.star-rating::attr(class)", default="star-rating Zero")
        loader.add_css("upc", "table.table.table-striped tr:nth-child(1) td::text", default="")
        
        item = loader.load_item()

        for field in ["title", "price", "availability", "description", "category", "rating", "upc"]:
            if field not in item:
                if field == "price":
                    item[field] = 0.0
                elif field == "rating":
                    item[field] = 0
                elif field == "stock_count":
                    item[field] = 0
                else:
                    item[field] = ""

        yield item
        