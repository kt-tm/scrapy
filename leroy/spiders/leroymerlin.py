import scrapy
from scrapy.http import HtmlResponse
from leroy.items import LeroyItem
from scrapy.loader import ItemLoader


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super(LeroymerlinSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']
        print(1)

    def parse(self, response:HtmlResponse):
        ads_links = response.xpath("//a[@slot='picture']")
        print(f"ads_links={ads_links}")
        for ads in ads_links:
            yield response.follow(ads, callback=self.parse_ads)


    def parse_ads(self, response:HtmlResponse):
        loader = ItemLoader(item=LeroyItem(), response=response)
        loader.add_xpath('photos',"//img[@slot='thumbs']/@src")
        loader.add_xpath('name',"//h1/text()")
        loader.add_xpath('price', "//meta[@itemprop='price']/@content")
        loader.add_xpath('characteristic_key', "//section[@class='pdp-section pdp-section--product-characteristicks']//dt[@class='def-list__term']/text()")
        loader.add_xpath('characteristic_val',
                         "//section[@class='pdp-section pdp-section--product-characteristicks']//dd[@class='def-list__definition']/text()")
        yield loader.load_item()