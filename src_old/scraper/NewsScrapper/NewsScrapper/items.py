# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    category = scrapy.Field()
    thumbnail = scrapy.Field()
    content = scrapy.Field()
    
