# -*- coding: utf-8 -*-

from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst


def clean_price(price):
    """
    Clean a price string by removing the pound sign and stripping
    whitespace. If the result cannot be converted to a float, return 0.0.
    """

    try:
        return float(price.replace("£", "").strip())
    except:
        return 0.0
    

def clean_availability(avail):
    """
    Clean an availability string by stripping whitespace.
    """
    return avail.strip()


class BooksInformationsLoader(ItemLoader):

    default_output_processor = TakeFirst()
    price_in = MapCompose(clean_price)
    availability_in = MapCompose(clean_availability)