from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroy.spiders.leroymerlin import LeroymerlinSpider
from leroy import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinSpider, search='новогодняя ель')

    process.start()
