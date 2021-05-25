import scrapy
from scrapy.crawler import CrawlerProcess
from termcolor import colored
from gpu_bot.spiders.stock_check import stockCheckSpider 
from bots.bestbuy import GetBestbuyStock
import time
from bot_email.send_email import SendEmail
import re
import os 

class BreakOut(Exception): pass

def main():
    process  = CrawlerProcess()
    process.crawl(stockCheckSpider)
    process.start()

    gpus = GetBestbuyStock()

    if bool(gpus):
        SendEmail(gpus)

    if os.stat('gamestop_stock.json') != 0:
        with open('gamestop_stock.json', 'r+') as stock:
            print(colored(stock.readlines(),'green'))
#            first_line = stock.readlines()[1]
#            SendEmail(first_line)
            stock.truncate(0)

if __name__ == '__main__':
    main()
