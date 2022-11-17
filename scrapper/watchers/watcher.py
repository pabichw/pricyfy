'''watcher module'''
from threading import Thread

import requests
from bs4 import BeautifulSoup

from const.options import SCRAPPING_INTERVAL_SECONDS
from db import db
from utils.sender import EmailTemplates, Sender
from utils.product import ProductUtil
from sel import sel
import os
from selenium.webdriver.common.by import By

headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}


class Error(Exception):
    '''Generic Error'''
    pass


class NoElemFoundExcpetion(Error):
    '''Used when no element found'''
    pass


class Watcher(Thread):
    '''Generic class to handle generic watcher problems. It should extend other, more site-specific watchers.'''

    soup = None
    stopped = None
    URL = None

    def __init__(self, event, URL):
        Thread.__init__(self)
        self.stopped = event
        self.product_id = None
        self.url = URL

        db_product = ProductUtil.get_db_entity({"url": self.url})

        if db_product.get('status', None) == 'INACTIVE':
            self.stop()
        else:
            try:
                self.take_screenshot()
            except:
                print(
                    f'[WARN] Unable to take screenshot for {self.url}')

    def run(self):
        while not self.stopped.wait(SCRAPPING_INTERVAL_SECONDS):
            try:
                self.scrap()
            except NoElemFoundExcpetion as exception:
                print('ARGHH!', exception,
                      '\nBut I will keep cracking chief! (＠＾◡＾)')

    def get_page(self):
        '''get content of a page'''

        page = requests.get(self.url, headers=headers)
        self.soup = BeautifulSoup(page.content, 'lxml')

    def check_notify(self, price_parsed, prod_title):
        # TODO: divide check and send
        '''Decide if condition fulfilled (to be moved) and send email'''

        db_product = ProductUtil.get_db_entity({"url":  self.url})

        if self.check_drop_requirements(data={'price_parsed': price_parsed, 'db_product': db_product}):
            print('[INFO] Sending price drop email (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧')

            Sender.send_mail(
                variables={
                    'prod_title': prod_title,
                    'last_price': ProductUtil.get_current_price(db_product),
                    'url': self.url,
                    'price': price_parsed,
                },
                to=db_product.get('recipients', []),
                type=EmailTemplates.PRICE_DROP)

        elif self.check_raise_requirements(data={'price_parsed': price_parsed, 'db_product': db_product}):
            print('[INFO] Sending price raise email :(')

            Sender.send_mail(
                variables={
                    'prod_title': prod_title,
                    'last_price': ProductUtil.get_current_price(db_product),
                    'url': self.url,
                    'price': price_parsed,
                },
                to=db_product.get('recipients', []),
                type=EmailTemplates.PRICE_RAISE)

        self.update_last_price(price_parsed)

    def scrap(self):
        '''overloaded in site-specific watchers'''
        self.get_page()
        pass

    def check_inactive(self):
        '''overloaded in site-specific watchers'''
        pass

    def mark_as_inactive(self):
        '''mark product as inactive'''

        db.get_db()['products'].update_one(
            {"url": self.url}, {"$set": {'status': "INACTIVE"}})

    def add_product_id(self, product_id):
        '''adds product_id to entry when harvested'''

        db.get_db()['products'].update_one(
            {"url": self.url}, {"$set": {'product_id': product_id}})

    def check_drop_requirements(self, data={}):
        '''checks for notify requirements. Can be overriden by specific watcher method'''

        return data.get('price_parsed') < ProductUtil.get_current_price(data.get('db_product'))

    def check_raise_requirements(self, data={}):
        '''checks for notify requirements. Can be overriden by specific watcher method'''

        return data.get('price_parsed') > ProductUtil.get_current_price(data.get('db_product'))

    def update_last_price(self, price):
        '''updates last price'''

        # update self.price also?
        db.get_db()['products'].update_one(
            {"product_id": self.product_id}, {"$set": {'last_found_price': price}})

    def take_screenshot(self):
        '''takes screenshot of an offer'''

        driver = sel.get_selenium()
        driver.get(self.url)
        id = ProductUtil.get_db_entity({"url": self.url}).get('product_id')

        print(f'Screenshot: {id}')

        # delete onetrust node onetrust-consent-sdk TODO: extract to OLX
        # NOTE: dla otodom jest inny id "_next"
        one_trust = driver.find_element(By.ID, 'onetrust-consent-sdk')
        if one_trust:
            driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, one_trust)

        driver.find_element(By.TAG_NAME, 'body').screenshot(
            os.getcwd() + f'/screenshots/{id}.png')

    def stop(self, send_email=False):
        '''stops thread'''

        print('Stopping: ', self.url)

        if send_email:
            print('Sending abort mail...')

            db_product = ProductUtil.get_db_entity({"url":  self.url})

            Sender.send_mail(
                variables={'url': self.url,
                           'last_price': db_product.get('last_found_price')},
                to=db_product.get('recipients', []),
                type=EmailTemplates.WATCH_CANCELLED)

        self.stopped.set()
