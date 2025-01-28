import pymongo
import scrapy
import re

from scrapy.crawler import CrawlerProcess
from urllib.parse import urljoin


class MySpider(scrapy.Spider):
    name = "myspider"
    start_urls = ["https://books.toscrape.com/"]

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["Bibliometrics"]
        self.collection = self.db["Books"]

    def parse(self, response):
        category_links = response.css(
            ".side_categories ul li ul li a::attr(href)"
        ).extract()
        for category_link in category_links:
            yield scrapy.Request(
                urljoin(response.url, category_link), callback=self.parse_category
            )

    def parse_category(self, response):
        category = response.css("h1::text").get()
        book_links = response.css("h3 a::attr(href)").extract()
        for book_link in book_links:
            yield scrapy.Request(
                urljoin(response.url, book_link),
                callback=self.parse_book,
                meta={"category": category},
            )

        next_page = response.css(".next a::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(
                urljoin(response.url, next_page), callback=self.parse_category
            )

    def parse_book(self, response):
        category = response.meta["category"]
        title = response.css("h1::text").get()
        price_with_currency = response.css(".price_color::text").get()
        price = float(re.search(r"[\d.]+", price_with_currency).group())
        cover_book = urljoin(
            response.url, response.css(".thumbnail img::attr(src)").get()
        )
        rating_class = response.css(".star-rating::attr(class)").get()
        rating = self.extract_rating(rating_class)
        stock_element = response.xpath(
            '//th[text()="Availability"]/following-sibling::td/text()'
        ).get()
        available_stock = (
            int(re.search(r"\d+", stock_element).group()) if stock_element else None
        )
        description = response.xpath(
            '//div[@id="product_description"]/following-sibling::p/text()'
        ).get()

        self.collection.insert_one(
            {
                "title": title,
                "price": price,
                "rating": rating,
                "available_stock": available_stock,
                "description": description,
                "category": category,
                "cover_book": cover_book,
            }
        )

    def extract_rating(self, rating_class):
        rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        rating_value = rating_class.split()[1]
        return rating_map.get(rating_value, None)


process = CrawlerProcess()
process.crawl(MySpider)
process.start()
