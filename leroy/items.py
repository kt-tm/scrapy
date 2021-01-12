# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def process_photos(photo):
    try:
        photo = photo.replace('w_82','w_2000').replace('h_82','h_2000')
        print(f"photo={photo}")
        return photo
    except:
        return photo

class LeroyItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor = TakeFirst())
    price = scrapy.Field(output_processor = TakeFirst())
    photos = scrapy.Field(input_processor = MapCompose(process_photos))
    characteristic = scrapy.Field(output_processor = TakeFirst())
    characteristic_key = scrapy.Field()
    characteristic_val = scrapy.Field()
    _id = scrapy.Field()
