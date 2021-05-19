import requests
from requests.structures import CaseInsensitiveDict
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from bots.selenium_driver import SeleniumDriver

def neweggStockCheck(url):
    source = urllib.request.urlopen(url).read()

    sauce = BeautifulSoup(source, "lxml")


def bestbuyStockCheck(url):
    source = requests.get(url).content
    print('This is the source: ', source)


    sauce = BeautifulSoup(source, "lxml")
    print('this is the sauce: ', sauce)
           
def check(urls):
    for url in urls:
        if 'newegg' in url.lower():
            print('this is a newegg link')
        elif 'bestbuy' in url.lower():
            print('this is a bestbuy link')
            bestbuyStockCheck(url)
