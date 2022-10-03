'''watcher module'''
from threading import Thread

import requests
from bs4 import BeautifulSoup

from const.options import SCRAPPING_INTERVAL_SECONDS
from db import db
from utils.sender import Sender

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

    price = 0
    soup = None
    stopped = None
    URL = None

    def __init__(self, event, URL, price):
        Thread.__init__(self)
        self.stopped = event
        self.price = price
        self.product_id = None
        self.url = URL

        db_product = db.get_db()['products'].find_one({"url":  URL})
        if db_product.get('status', None) == 'INACTIVE':
            self.stop()

        page = requests.get(URL, headers=headers)
        self.soup = BeautifulSoup(page.content, 'lxml')

    def run(self):
        while not self.stopped.wait(SCRAPPING_INTERVAL_SECONDS):
            try:
                self.scrap()
            except NoElemFoundExcpetion as exception:
                print('ARGHH!', exception,
                      '\nBut I will keep cracking chief! (＠＾◡＾)')

    def send_if_fulfilled(self, price_parsed, prod_title):
        # TODO: divide check and send
        '''Decide if condition fulfilled (to be moved) and send email'''

        if price_parsed < self.price:
            print('[INFO] Sending email (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧')

            db_product = db.get_db()['products'].find_one(
                {"url":  self.url})

            Sender.send_mail(
                prod_title,
                price_parsed,
                self.price,
                self.url,
                to=db_product.get('recipients', []))

            self.price = price_parsed
            # time.sleep(SLEEP_AFTER_SEND)

        db.get_db()['products'].update_one(
            {"product_id": self.product_id}, {"$set": {'last_found_price': price_parsed}})

    def scrap(self):
        '''overloaded in site-specific watchers'''
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

    def stop(self):
        '''stops thread'''

        print('Stopping: ', self.url)
        self.stopped.set()
