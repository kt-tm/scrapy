import scrapy


class LeroymerlinSpider(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field()
    characteristic = scrapy.Field()
    link = scrapy.Field()
    photos = scrapy.Field()
    _id = scrapy.Field()