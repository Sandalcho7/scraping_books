import scrapy
from scrapy.crawler import CrawlerProcess
from items import BookItem
import json
from urllib.parse import urljoin

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):
        # Extract category links
        category_links = response.css('.side_categories ul li ul li a::attr(href)').extract()

        # Follow each category link
        for category_link in category_links:
            yield scrapy.Request(response.urljoin(category_link), callback=self.parse_category)

    def parse_category(self, response):
            # Extract category name
        category = response.css('h1::text').get()

            # Extract book titles and cover image URLs in the category
        books = response.css('.product_pod')

        for book in books:
            title = book.css('h3 a::attr(title)').get()
            cover_book_relative = book.css('img::attr(src)').get()
            cover_book=response.urljoin(cover_book_relative)
            item = BookItem(category=category, title=title, cover_book=cover_book)
            yield item


process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': './json/books3.json'
})

process.crawl(MySpider)
process.start()

# Load the scraped data from the JSON file


with open('./json/books3.json', 'r') as f:
    data = json.load(f)

# Process the data to create the desired dictionary
category_dict = {}

for item in data:
    category = item['category']
    title = item['title']
    cover_books = item['cover_book']
    
    if category not in category_dict:
        category_dict[category] = []
    
    category_dict[category].append(title)
    sorted_categories = sorted(category_dict.keys())

# Create a new dictionary with sorted categories
    sorted_category_dict = {category: category_dict[category] for category in sorted_categories}

print(cover_books)
print(sorted_category_dict)
# print(category_dict)




