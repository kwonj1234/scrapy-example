import scrapy

class QuotesSpider(scrapy.Spider):
    name = "stocks"
    start_urls = [
        'https://markets.businessinsider.com/stocks',
    ]

    def parse(self, response):
        count = 0
        stocks_dict = {
            "Market_Movers" : {},
            "Top_Market_Caps" : {},
        }
        # Scrape tables and tr tags on the page. tr tags are used to show
        # data, but is also used for forms on this page so not all tr tags
        # have relevant data
        table_rows = response.css('table.table').xpath('./tr')
        # All tr tags with children a tag have company names. There should
        # be 25 names for each relevant table row
        # 10 for market movers
        # 10 for top market caps
        # 10 for top dividents
        company_names = table_rows.css('a::text').getall()
        # Market Mover data
        # rel_data contains both price and time stamp, the site uses the 
        # same tag and class for both
        rel_data = table_rows.css('div.text-nowrap::text').getall()
        # change contains both percent change and actual change
        change = table_rows.css('div.text-nowrap').xpath('./span/text()').getall()
        # Top Market Cap data
        cap = table_rows.css('td.text-right::text').getall()
        # The rest of the rows contains another table called top 
        # dividends, it is not as complicated as the other two so I 
        # skipped it because if you can scrape the prior two tables,
        # you most certainly scrape this one 
        market_movers = {}
        market_caps = {}
        for i in range(len(company_names)):
            if 0 <= i < 10:
                price_index = percent_index = i * 2
                time_index = change_index = price_index + 1
                temp_dict = {
                    "company_name"  : company_names[i],
                    "price"         : rel_data[price_index],
                    "time_stamp"    : rel_data[time_index],
                    "percent_change": change[percent_index],
                    "change"        : change[change_index]
                }
                market_movers[i] = temp_dict
            elif 10 <= i < 19:
                cap_index = i - 10
                temp_dict = {
                    'company_name' : company_names[i],
                    'cap'          : cap[cap_index]
                }
                market_caps[i] = temp_dict
        # Store scraped data in main dictionary and store it
        stocks_dict["Market_Movers"] = market_movers
        stocks_dict["Top_Market_Caps"] = market_caps
        # Take the time to write out the yield statement, scrapy does not
        # format the JSON file nicely. All the data will be on one line
        # doing this
        # yield stocks_dict
        yield {
            "Market_Movers"  : market_movers,
            "Top_Market_Caps": market_caps
        }