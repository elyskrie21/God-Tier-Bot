import scrapy
from scrapy.selector import Selector
import re
from gpu_bot.items import GpuBotItem
from termcolor import colored
from bs4 import BeautifulSoup

class stockCheckSpider(scrapy.Spider):
    name = 'stock_check'

    custom_settings = {
        'FEED_URI': 'gamestop_stock.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORTERS': {
            'json': 'scrapy.exporters.JsonItemExporter',
        },
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    start_urls = ['https://www.gamestop.com/search/?q=3060&lang=default', 'https://www.gamestop.com/search/?q=3070&lang=default']


    def parse(self, response):
        sauce = BeautifulSoup(response.body, 'lxml')
        for gpu in sauce.find_all('div', class_='product-grid-tile-wrapper'):
            gpus = GpuBotItem()

            gpus['name'] = gpu.find(class_='pd-name').get_text()
            gpus['available'] = gpu.find('div', {'data-available': 'false'}) is None           
            gpus['link'] = response.url
            
            if gpus['available'] == True:
                yield gpus 

            next_page = None
            if next_page is not None:
                yield response.follow(next_page, self.parse)

class bhCheckSpider(scrapy.Spider):
    name = 'bestboy_stock'

    custom_settings = {
        'FEED_URI': 'gpu_stock.json',
        'FEED_FORMAT': 'json', 
        'FEEd_EXPORTERS': {
            'json': 'scrapy.exporters.JsonItemExporter',
        },
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    start_urls = ['https://www.bestbuy.com']

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,fr;q=0.8', 
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://www.google.com/',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site', 
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }


    def parse(self, response):
        url = 'https://www.bestbuy.com/site/searchpage.jsp?id=pcat17071&st=xbox+series+x'
        
        yield scrapy.Request(url, callback=self.parse_api, headers = self.headers)


    def parse_api(self, response):
        yield response.body


