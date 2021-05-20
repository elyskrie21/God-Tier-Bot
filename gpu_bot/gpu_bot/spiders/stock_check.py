import scrapy


class StockCheckSpider(scrapy.Spider):
    name = 'stock_check'
    allowed_domains = ['https://www.bestbuy.com/site/searchpage.jsp?st=graphics+card']
    start_urls = ['http://https://www.bestbuy.com/site/searchpage.jsp?st=graphics+card/']

    def parse(self, response):
        pass
