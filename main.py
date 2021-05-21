import scrapy
from scrapy.crawler import CrawlerProcess
import re
from termcolor import colored
from gpu_bot.spiders.stock_check import stockCheckSpider 

def main():
    process = CrawlerProcess()
    process.crawl(stockCheckSpider)
    
    data = process.start()

    with open('gamestop_stock.json', 'r+') as stock:
        print(colored(stock.readlines()[1], 'blue'))
        stock.truncate(0)

if __name__ == '__main__':
    main()
