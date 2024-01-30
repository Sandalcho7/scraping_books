import scrapy
from scrapy.crawler import CrawlerProcess
from items import BookItem
from pymongo import MongoClient
import json
from urllib.parse import urljoin


class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://books.toscrape.com/']
    total_books = None  # Variable pour stocker le nombre total de livres

    def __init__(self):
        super(MySpider, self).__init__()
        self.visited_books = set()  # Pour garder une trace des livres déjà collectés

    def parse(self, response):
        # Extract category links
        category_links = response.css('.side_categories ul li ul li a::attr(href)').extract()

        # Follow each category link
        for category_link in category_links:
            yield scrapy.Request(response.urljoin(category_link), callback=self.parse_category)

        # Estimer le nombre total de livres sur le site
        if self.total_books is None:
            self.total_books = self.estimate_total_books(response)
            print("Nombre total de livres disponibles sur le site web (estimation) :", self.total_books)

    def parse_category(self, response):
        # Extract category name
        category = response.css('h1::text').get()

        # Extract book titles and cover image URLs in the category
        books = response.css('.product_pod')

        for book in books:
            title = book.css('h3 a::attr(title)').get()
            cover_book_relative = book.css('img::attr(src)').get()
            cover_book = response.urljoin(cover_book_relative)
            item = BookItem(category=category, title=title, cover_book=cover_book)
            yield item

        # Check for next page
        next_page = response.css('.next a::attr(href)').get()
        if next_page:
            yield scrapy.Request(urljoin(response.url, next_page), callback=self.parse_category)

    def estimate_total_books(self, response):
        # Extracting the number of pages
        last_page_href = response.css('.pager li.last a::attr(href)').get()
        print("URL de la dernière page :", last_page_href)
        if last_page_href:
            last_page_number = int(last_page_href.split('/')[-1].split('.')[0].split('_')[-1])
            print("Numéro de la dernière page :", last_page_number)
            # Total books estimation
            return (last_page_number - 1) * 20 + len(response.css('.product_pod'))
        else:
            return 0


# Run the spider
process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': './json/books3.json'
})

process.crawl(MySpider)
process.start()

# Load the scraped data from the JSON file
with open('./json/books3.json', 'r') as f:
    data = json.load(f)

# Check if the JSON is empty
if not data:
    print("Le JSON est vide. Vérifiez les journaux du spider pour les erreurs.")

# Connect to MongoDB and insert the data if it's not empty
if data:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['bookstore']
    collection = db['books']
    collection.insert_many(data)
    print("Les données ont été insérées dans la base de données MongoDB avec succès.")
