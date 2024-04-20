
import datetime

db = client.scrapy


doc = {
    "author": "Mike",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.now(datetime.timezone.utc),
}
post_id = posts.insert_one(doc).inserted_id
