# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class Article(Item):
    url = Field()
    title = Field()
    text = Field()
    last_updated = Field(serializer=str)
