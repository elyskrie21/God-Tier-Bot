import scrapy
from scrapy.selector import Selector
import re
from gpu_bot.items import GpuBotItem
from termcolor import colored
from bots.selenium_driver import SeleniumDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

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

    start_urls = ['https://www.gamestop.com/search/?q=ps5&lang=default']

    def parse(self, response):
        for gpu in response.css('.product-grid-tile-wrapper'):
            gpus = GpuBotItem()

            gpus['name'] = gpu.css('.pd-name::text').get()
            gpus['price'] = re.sub('\D','',gpu.css('.actual-price::text').get())[:-2]
            gpus['available'] =  'sold out' not in gpu.css('.store-availability-msg::attr(class)').get() 
            
            print(colored(gpus, 'green'))

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

