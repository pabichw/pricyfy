import requests
from bs4 import BeautifulSoup
from threading import Thread, Event
import smtplib 
import csv
import time
from enum import Enum 
from urllib.parse import urlparse
import datetime

PRODUCTS_TO_WATCH = []
headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}
SCRAPPING_INTERVAL_SECONDS = 60 * 1 #5 minutes
SLEEP_AFTER_SEND = 60 * 30 #20 minutes

class SHOPS_DOMAINS(): 
    AMAZON = 'www.amazon.de'
    MEDIA_EXPERT = 'www.mediaexpert.pl'

class Product: 
    url = ''
    price = 0
    def __init__(self, url, price): 
        self.url = url
        self.price = price

class AmazonWatcher(Thread): 
    price = 0
    soup = None
    stopped = None
    URL = None

    def __init__(self, event, URL, price): 
        print(f'[INFO] Starting amazon watcher:\n URL: {URL}\n Price: {price}',)
        Thread.__init__(self)
        self.stopped = event

        page = requests.get(URL, headers=headers)
        self.soup = BeautifulSoup(page.content, 'html.parser')
        self.price = price
        self.URL = URL
    
    def run(self):
        while not self.stopped.wait(SCRAPPING_INTERVAL_SECONDS):
            self.scrap()

    def scrap(self):
        prodTitle = self.soup.find(id='productTitle').get_text().strip()
        price = self.soup.find(id='priceblock_ourprice').get_text()

        price = price.replace('\xa0€','').replace(',','.')
        priceFloat = float(price)
        print('[',datetime.datetime.now(),']','Amazon.de: ', prodTitle, ' : ', priceFloat, ' need: ', self.price)

        if priceFloat > self.price:
            print('[INFO] Sending email')
            Sender.send_mail(prodTitle, price, self.URL)
            time.sleep(SLEEP_AFTER_SEND)
    
class MediaExpertWatcher(Thread): 
    price = 0
    soup = None
    stopped = None
    URL = None

    def __init__(self, event, URL, price): 
        print(f'[INFO] Starting mediaexpert.pl watcher:\n URL: {URL}\n Price: {price}',)
        Thread.__init__(self)
        self.stopped = event

        page = requests.get(URL, headers=headers)
        self.soup = BeautifulSoup(page.content, 'html.parser')
        self.price = price
        self.URL = URL
    
    def run(self):
        while not self.stopped.wait(SCRAPPING_INTERVAL_SECONDS):
            self.scrap()

    def scrap(self):
        prodTitle = self.soup.findAll("h1", {'class': 'pv_title'})[0].text
        price = self.soup.findAll("p", {'class': 'price_txt'})[0].text

        priceFloat = float(price[:len(price) - 2] + '.' + price[len(price) - 2:])
        print('[',datetime.datetime.now(),']','Amazon.de: ', prodTitle, ' : ', priceFloat, ' need: ', self.price)
        print('priceFloat:', priceFloat, ' self.price:', self.price)
        if priceFloat > self.price:
            print('[INFO] Sending email')
            Sender.send_mail(prodTitle, price, self.URL)
            time.sleep(SLEEP_AFTER_SEND)
    
class Sender: 
    @staticmethod
    def composeMail(prodTitle, price, url):
        return f'Subject: Price of {prodTitle} fell down!\n\nPrice of {prodTitle} has just fell down to {price}! There is a direct link: {url}'.encode('utf-8')

    @staticmethod
    def send_mail(prodTitle, price, url):
        server = smtplib.SMTP('mail28.mydevil.net', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('bot@pabich.cc', 'Prometeusz213') #TODO: Hash it
        server.sendmail('bot@pabich.cc', 'pabichwiktor@gmail.com', Sender.composeMail(prodTitle, price, url))
        server.quit()


def watch(URL, price):
    stop_flag = Event()
    domain = urlparse(URL).netloc

    threadHandler = Thread()
    if domain == SHOPS_DOMAINS.AMAZON:
        threadHandler = AmazonWatcher(stop_flag, URL, price)
    elif domain == SHOPS_DOMAINS.MEDIA_EXPERT:
        threadHandler = MediaExpertWatcher(stop_flag, URL, price)
    threadHandler.start()

def loadProducts():
    print('[INFO] Loading proasdasducts...')
    with open('products.csv', newline='') as products_csv:
        print('a')
        reader = csv.reader(products_csv, delimiter=' ', quotechar='|')
        print('b')
        for row in reader:
            PRODUCTS_TO_WATCH.append(Product(row[0], float(row[1])))

if __name__ == "__main__":
    loadProducts()
    print(PRODUCTS_TO_WATCH)
    list(map(lambda product: watch(product.url, product.price), PRODUCTS_TO_WATCH))