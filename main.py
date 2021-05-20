import scrapy
from scrapy.crawler import CrawlerProcess
import re
from termcolor import colored
from gpu_bot.spiders.stock_check import stockCheckSpider 

def main():
    process = CrawlerProcess()
    process.crawl(stockCheckSpider)
    
    data = process.start()
    print(colored(data, 'red'))

if __name__ == '__main__':
    main()
