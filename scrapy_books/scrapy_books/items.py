# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksInformations(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    availability = scrapy.Field()
    stock_count = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    rating = scrapy.Field()
    upc = scrapy.Field()
