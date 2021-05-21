import scrapy
import re
from gpu_bot.items import GpuBotItem
from termcolor import colored

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

