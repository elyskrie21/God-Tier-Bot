from data.urls import urls
from scrapers.stock_check import check

print(urls)

print('starting')
check(urls)
print('finished')
