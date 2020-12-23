import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82+python']

    def parse(self, response: HtmlResponse):
        vacancies_links = response.xpath("//div[@class='vacancy-serp-item__info']//a/@href").extract()

        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_parse)

        next_page = response.xpath("//a[contains(@class,'HH-Pager-Controls-Next')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").extract_first()
        salary = response.xpath("//p[@class='vacancy-salary']//span/text()").extract()
        link = response.url
        yield JobparserItem(name=name, salary=salary, link=link)
