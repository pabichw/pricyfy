import datetime
import time
from threading import Thread

import requests
from bs4 import BeautifulSoup

from const.options import SCRAPPING_INTERVAL_SECONDS, SLEEP_AFTER_SEND
from utils.sender import Sender

headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}


class Watcher(Thread):
    price = 0
    soup = None
    stopped = None
    URL = None

    def __init__(self, event, URL, price):
        Thread.__init__(self)
        self.stopped = event

        page = requests.get(URL, headers=headers)
        self.soup = BeautifulSoup(page.content, 'lxml')
        self.price = price
        self.URL = URL

    def run(self):
        while not self.stopped.wait(SCRAPPING_INTERVAL_SECONDS):
            try:
                self.scrap()
            except:
                print(f'Unexpected result of scrapping {self.URL}\nBut I will keep cracking chief! 	(＠＾◡＾)')

    def sendIfFulfilled(self, price_parsed, prod_title):
        print('[', datetime.datetime.now(), ']', 'Amazon.de: ', prod_title, ' : ', price_parsed, ' need: ', self.price)
        if price_parsed < self.price:
            print('[INFO] Sending email (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧')
            Sender.send_mail(prod_title, price_parsed, self.URL)
            time.sleep(SLEEP_AFTER_SEND)