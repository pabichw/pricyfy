import requests
from bs4 import BeautifulSoup
from threading import Thread, Event
import smtplib 
import csv
import time

PRODUCTS_TO_WATCH = []
headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}
SCRAPPING_INTERVAL_SECONDS = 5 #half an hour
SLEEP_AFTER_SEND = 60 * 20 #20 minutes

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
        print(f'[INFO] Starting Amazon watcher:\n URL: {URL}\n Price: {price}',)
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
        print(prodTitle, '\n', price)

        priceFloat = float(price)
        if priceFloat < self.price:
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
    amazonHandler = AmazonWatcher(stop_flag, URL, price)
    amazonHandler.start()

def loadProducts():
    print('[INFO] Loading products...')
    with open('products.csv', newline='') as products_csv:
        reader = csv.reader(products_csv, delimiter=' ', quotechar='|')
        for row in reader:
            print('row:',row)
            PRODUCTS_TO_WATCH.append(Product(row[0], float(row[1])))

if __name__ == "__main__":
    loadProducts()
    print(PRODUCTS_TO_WATCH)
    list(map(lambda product: watch(product.url, product.price), PRODUCTS_TO_WATCH))
