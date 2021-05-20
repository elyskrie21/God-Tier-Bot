import scrapy
import re
from gpu_bot.items import GpuBotItem
from termcolor import colored

class stockCheckSpider(scrapy.Spider):
    name = 'stock_check'
    start_urls = ['https://www.gamestop.com/search/?q=camera&lang=default']

    def parse(self, response):
        for gpu in response.css('.product-grid-tile-wrapper'):
            gpus = GpuBotItem()

            gpus['name'] = gpu.css('.pd-name::text').get()
            gpus['price'] = re.sub('\D','',gpu.css('.actual-price::text').get())[:-2]
            gpus['available'] = 'sold-out' not in re.sub('\D','',gpu.css('.actual-price::text').get())[:-2]
            print(colored(gpus, 'green'))


            next_page = None
            if next_page is not None:
                yield response.follow(next_page, self.parse)

        yield this.returnValue(gpus)
    
    def returnValue(value):
        return value


