import scrapy

class QuotesSpider(scrapy.Spider):
    name = "stocks"
    start_urls = [
        'https://markets.businessinsider.com/stocks',
    ]

    def parse(self, response):
        for row in response.css('table.table').xpath('./tr'):
            print(row)
            