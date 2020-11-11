import scrapy

class QuotesSpider(scrapy.Spider):
    name = "stocks"
    start_urls = [
        'https://markets.businessinsider.com/stocks',
    ]

    def parse(self, response):
        count = 0
        stocks_dict = {
            "Market Movers" : {},
            "Top Market Caps" : {},
            "Top Dividens" : {}
        }
        for row in response.css('table.table').xpath('./tr'):
            market_movers_list = []
            market_caps = []
            if 0 <= count < 10:
                company_name = row.css('a::text').get()
                # Price and time stamp are located inside a div with class 
                # text-nowrap
                nowrap_css = row.css('div.text-nowrap::text').getall()
                price = nowrap_css[0]
                time_stamp = nowrap_css[1]
                # Percent change lives in a span within the text-nowrap div
                # There are multiple spans within div.text-nowrap but we 
                # know percent change is always the first within the row
                # so we can use the .get() to retrieve the first instance
                percent_change = row.css('div.text-nowrap')
                                 .xpath('./span/text()').get()
                temp_dict = {
                    "company name"  : company_name,
                    "price"         : price,
                    "time_stamp"    : time_stamp,
                    "percent_change": percent_change
                }
                market_movers_list.append(temp_dict)
            if 10 <= count < 19:

            