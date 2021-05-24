import scrapy
from scrapy.crawler import CrawlerProcess
from termcolor import colored
from gpu_bot.spiders.stock_check import stockCheckSpider, bestbuyCheckSpider 
import time


def main():
    process  = CrawlerProcess()
    process.crawl(stockCheckSpider)
    process.crawl(bestbuyCheckSpider)
    process.start()

    with open('gamestop_stock.json', 'r+') as stock:
        print(colored(stock.readlines()[1], 'blue'))
        stock.truncate(0)

if __name__ == '__main__':
    main()
