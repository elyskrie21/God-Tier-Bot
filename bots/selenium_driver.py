from selenium.webdriver.common.by import By
from traceback import print_stack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import logging
import sys


class SeleniumDriver():
    def __init__(self, driver, is_verbose=False):
        self.driver = driver

        if (is_verbose):
            self.log_level = logging.DEBUG
        else:
            self.log_level = logging.INFO
        log_format = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] - %(message)s')
        self.log = logging.getLogger(__name__)
        self.log.setLevel(self.log_level)

        # writing to stdout
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(self.log_level)
        handler.setFormatter(log_format)
        self.log.addHandler(handler)

    def getTitle(self): return self.driver.title
    def get(self, url): return self.driver.get(url)
    def getPageSource(self): return self.driver.page_source

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == 'id':
            return By.ID
        elif locatorType == 'name':
            return By.NAME
        elif locatorType == 'xpath':
            return By.XPATH
        elif locatorType == 'class':
            return By.CLASS_NAME
        elif locatorType == 'link':
            return By.LINK_TEXT
        else:
            self.log.info(f'Locator type ${locatorType} not correct/supported')
        return False

    def getElement(self, locator, locatorType='id'):
        element = None

        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.log.info(
                f'Element found with locator: ${locator} and locatorType: ${locatorType}')
        except:
            self.log.info(
                f'Element was not found with locator: ${locator} and locatorType: ${locatorType}')
        return element

    def getElements(self, locator, locatorType='id'):
        elements = []

        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            elements = self.driver.find_elements(byType, locator)
            self.log.info(
                f'Elements found with locator: ${locator} and locatorType: ${locatorType}')
        except:
            self.log.info(
                f'Elements were not found with locator: ${locator} and locatortype: ${locatorType}')
        return elements

    def elementClick(self, locator, locatorType='id'):
        try:
            element = self.getElement(locator, locatorType)
            element.click()
            self.log.info(
                f'clicked on element with locator: ${locator} and locatorType: ${locatorType}')
        except:
            self.log.info(
                f'Cannot click on the element with locator: ${locator} and locatorType: ${locatorType}')
            print_stack()

    def sendKeys(self, data, locator, locatorType='id'):
        try:
            element = self.getElement(locator, locatorType)
            element.send_keys(data)
            self.log.info(
                f'Sent data on element with locator: ${locator} and locatorType: ${locatorType}')
        except:
            self.log.info(
                f'Cannot send data on element with locator: ${locator} and locatorType: ${locatorType}')
            # print_stack()

    def isElementPresent(self, locator, locatorType='id'):
        try:
            element = self.getElement(locator, locatorType)
            if element is not None:
                self.log.info('Element found')
                return True
            else:
                self.log.info('Element not found')
                return False
        except:
            self.log.info('Element not found')
            return False

    def elementPresenceCheck(self, locator, locatorType='id'):
        try:
            elements = self.getElements(locator, locatorType)
            if len(elements) > 0:
                self.log.info('Element Found')
                return True
            else:
                self.log.info('Element not found')
                return False
        except:
            self.log.info('Element not found')
            return False

    def waitForElement(self, locator, locatorType='id', timeout=10, pollFrquency=0.5):
        element = None

        try:
            byType = self.getByType(locatorType)
            self.log.info(
                f'Waiing for maximum :: ${str(timeout)} :: seconds for element to be clickable')
            wait = WebDriverWait(self.driver, timeout, poll_frequency=pollFrquency, ignored_exceptions=[
                                 NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((byType, locator)))
            self.log.info('Element appeared on the web page')
        except:
            self.log.info('Element did not appear on the web page')
            print_stack()
        return element
