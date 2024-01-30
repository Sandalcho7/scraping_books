import pymongo
import scrapy
import re
from scrapy.crawler import CrawlerProcess
from urllib.parse import urljoin

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://books.toscrape.com/']

    # Initialize the connection with MongoDB
    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["Bibliometrics"]

    def parse(self, response):
        # Extract category links
        category_links = response.css('.side_categories ul li ul li a::attr(href)').extract()

        # Follow each category link
        for category_link in category_links:
            yield scrapy.Request(response.urljoin(category_link), callback=self.parse_category)

    def parse_category(self, response):
        # Extract book links
        book_links = response.css('h3 a::attr(href)').extract()

        # Follow each book link
        for book_link in book_links:
            yield scrapy.Request(response.urljoin(book_link), callback=self.parse_book)

    def parse_book(self, response):
        # Extract book details
        title = response.css('h1::text').get()
        price_with_currency = response.css('.price_color::text').get()
        price = float(re.search(r'[\d\.]+', price_with_currency).group())

        # Extracting rating
        rating_class = response.css('.star-rating::attr(class)').get()
        rating = self.extract_rating(rating_class)

        # Extracting available stock
        stock_element = response.xpath('//th[text()="Availability"]/following-sibling::td/text()').get()
        available_stock = int(re.search(r'\d+', stock_element).group()) if stock_element else None

        # Extracting description
        description = response.xpath('//div[@id="product_description"]/following-sibling::p/text()').get()

        # Insert the scraped data into MongoDB
        category = response.css('.breadcrumb li:nth-child(3) a::text').get()
        collection = self.db[category]

        # Insert new data
        collection.insert_one({
            "title": title,
            "price": price,
            "rating": rating,
            "available_stock": available_stock,
            "description": description,
        })

    def extract_rating(self, rating_class):
        # Mapping between CSS classes and ratings
        rating_map = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }

        # Extract the rating value from the class attribute
        rating_value = rating_class.split()[1]

        # Use the extracted rating value as a key in the rating_map dictionary
        return rating_map.get(rating_value, None)


process = CrawlerProcess()
process.crawl(MySpider)
process.start()