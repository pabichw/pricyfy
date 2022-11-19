'''watcher module'''
from threading import Thread

import requests
from bs4 import BeautifulSoup

from const.options import SCRAPPING_INTERVAL_SECONDS
from db import db
from utils.sender import EmailTemplates, Sender
from utils.product import ProductUtil

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

    product_id = None
    soup = None
    stopped = None
    URL = None

    def __init__(self, event, URL):
        Thread.__init__(self)
        self.stopped = event
        self.url = URL

        db_product = ProductUtil.get_db_entity({"url": self.url})

        print(
            f'initing {self.url} product_id is {db_product.get("product_id", None)}')
        if not db_product.get('product_id', None):
            self.add_product_id(product_id=Watcher.create_id(self.url))

        print('----product----')
        print(ProductUtil.get_db_entity({"url": self.url}))

        db_product = ProductUtil.get_db_entity({"url": self.url})  # refresh
        self.product_id = db_product.get('product_id', None)

        if db_product.get('status', None) == 'INACTIVE':
            self.stop()

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

    @staticmethod
    def create_id(url):
        return url.rsplit('/', 1)[-1].replace('.html', '')

    def update_last_price(self, price):
        '''updates last price'''

        print(f'updating update_last_price {self.product_id} with {price}')

        db.get_db()['products'].update_one(
            {"product_id": self.product_id}, {"$set": {'last_found_price': price}})

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
