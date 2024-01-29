# items.py

import scrapy

class BookItem(scrapy.Item):
    category = scrapy.Field()
    title = scrapy.Field()
    cover_book = scrapy.Field()
