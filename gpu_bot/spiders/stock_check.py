import scrapy
from scrapy.selector import Selector
import re
from gpu_bot.items import GpuBotItem
from termcolor import colored
from bs4 import BeautifulSoup
import logging 

logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)

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

class bestbuyCheckSpider(scrapy.Spider):
    name = 'bestboy_stock'
    start_urls = ['https://www.bestbuy.com/site/searchpage.jsp?id=pcat17071&st=3070+rtx']

    custom_settings = {
        'FEED_URI': 'gpu_stock.json',
        'FEED_FORMAT': 'json', 
        'FEEd_EXPORTERS': {
            'json': 'scrapy.exporters.JsonItemExporter',
        },
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = SeleniumDriver(webdriver.Chrome(
            ChromeDriverManager().install(), options=options))

    def parse(self, response):
        data = self.driver.get(response.url)
        source = self.driver.getPageSource()
        print(colored('now parsing data', 'blue'))
        for gpu in Selector(source).css('.list-item'):
            gpus = GpuBotItem()

            gpus['name'] = gpu.css('.sku-header a::text').get()

            print(colored(gpus, 'red'))
            
            yield gpus 

            next_page = None
            if next_page is not None:
                yield response.follow(next_page, self.parse)

    def parse_result(self, response):
        print(colored(response.text, 'green'))
        
        for gpu in response.css('.list-item'):
            gpus = GpuBotItem()

            gpus['name'] = gpu.css('.sku-header a::text').get()

            print(colored(gpus, 'red'))
            
            yield gpus 

            next_page = None
            if next_page is not None:
                yield response.follow(next_page, self.parse)

