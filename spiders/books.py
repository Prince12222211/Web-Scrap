import scrapy
from pathlib import Path
from pymongo import MongoClient
import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client.scrapy


def insertToDb(page, title, rating, image, price, inStock):
    collection = db[page]
    doc = {
        "title": title,
        "rating": rating,
        "image": image,
        "price": price,
        "inStock": inStock,
        "date": datetime.datetime.utcnow()
    }
    inserted = collection.insert_one(doc)
    return inserted.inserted_id


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = [
        "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"books-{page}.html"

        # Save the file
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")

        # Extracting data from response using CSS selector
        cards = response.css('.product_pod')
        for card in cards:
            title = card.css("h3>a::text").get()
            rating = card.css(".star-rating::attr(class)").get().split()[-1]
            image = card.css(".image_container img::attr(src)").get()
            price = card.css(".price_color ::text").get()
            availability = card.css(".availability")
            if len(availability.css(".icon-ok")) > 0:
                inStock = True
            else:
                inStock = False

            # Insert data into MongoDB
            insertToDb(page, title, rating, image, price, inStock)


# Running the spider
if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess()
    process.crawl(BooksSpider)
    process.start()
