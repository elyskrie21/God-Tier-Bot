import requests
from requests.structures import CaseInsensitiveDict
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from ../urls import urls

while True:
    for url in urls:
        if url.lower().contains("newegg"):
            available = neweggStockCheck(url)
        elif url.lower().contains("bestbuy"):
            available = bestbuyStockStock(url)

        if 





