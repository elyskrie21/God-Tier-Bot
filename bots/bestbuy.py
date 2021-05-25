from bots.selenium_driver import SeleniumDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
from termcolor import colored 
import re 

options = webdriver.ChromeOptions()
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
driver = SeleniumDriver(webdriver.Chrome(ChromeDriverManager().install(), options=options))

start_urls = ['https://www.bestbuy.com/site/searchpage.jsp?id=pcat17071&st=rtx+3060+ti']

def GetBestbuyStock():
    driver.get(start_urls[0])
    sauce = BeautifulSoup(driver.getPageSource(), 'lxml')

    gpus = []
    for gpu in sauce.find_all('li', class_='sku-item'):
        #price = re.sub('\D','', gpu.find('span', class_='sr-only').get_text())[:-2]
        name = gpu.find('div', class_='sku-title').get_text()
        available = bool(gpu.find_all(string=re.compile('Add to Cart'), limit=1))
        link = 'bestbuy.com' + gpu.find('a').get('href')

        if available:
            gpus.append({
                'name': name,
                'link': link,
                'available': available
                }
            )
    print(gpus)

    driver.close()
    if bool(gpus):
        return gpus

