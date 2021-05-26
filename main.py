import scrapy
from scrapy.crawler import CrawlerProcess
from termcolor import colored
from gpu_bot.spiders.stock_check import stockCheckSpider 
from bots.bestbuy import GetBestbuyStock
from bot_email.send_email import SendEmail

class BreakOut(Exception): pass

def main():
    process  = CrawlerProcess()
    process.crawl(stockCheckSpider)
    process.start()

    gpus = GetBestbuyStock()

    if bool(gpus):
        SendEmail(gpus)

    with open('gamestop_stock.json', 'r+') as stock:
        try:
            first_line = stock.readlines()[1]
            SendEmail(first_line)
            stock.truncate(0)
        except IndexError:
            pass

if __name__ == '__main__':
    main()
