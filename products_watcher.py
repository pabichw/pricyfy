'''main watcher module'''
from threading import Thread, Event
import csv
import argparse
from urllib.parse import urlparse
from pymongo import MongoClient
import os
from dotenv import load_dotenv, find_dotenv

from const.shops_domains import ShopDomains
from models.product import Product
from watchers.amazon_watcher import AmazonWatcher
from watchers.media_expert_watcher import MediaExpertWatcher
from watchers.otodom_watcher import OtodomWatcher
from watchers.olx_watcher import OlxWatcher
from utils.logger import Logger

PRODUCTS_TO_WATCH = []


def watch(url, price):
    '''run watch process for each product'''
    stop_flag = Event()
    domain = urlparse(url).netloc

    thread_handler = Thread()
    if domain == ShopDomains.AMAZON:
        thread_handler = AmazonWatcher(stop_flag, url, price)
    elif domain == ShopDomains.MEDIA_EXPERT:
        thread_handler = MediaExpertWatcher(stop_flag, url, price)
    elif domain == ShopDomains.OTO_DOM:
        thread_handler = OtodomWatcher(stop_flag, url, price)
    elif domain == ShopDomains.OLX:
        thread_handler = OlxWatcher(stop_flag, url, price)
    # elif domain == SHOPS_DOMAINS.KOMPUTRONIK:
        # threadHandler = KomputronikWatcher(stop_flag, URL, price)
    else:
        print('Platform not supported: ', domain)
        return
    thread_handler.start()


def test_database():
    '''test database connection'''

    connection_string = os.environ.get("DATABASE_URL")

    client = MongoClient(connection_string)
    pricify = client['pricify']
    test_collection = pricify['test']
    insert = test_collection.insert_one({"foo": "bar"})

    print('---- DB test ----')
    print('Insert:', bool(insert))


def load_products():
    '''load products from source'''
    print('[INFO] Loading products...')
    with open('products.csv', newline='') as products_csv:
        reader = csv.reader(products_csv, delimiter=' ', quotechar='|')
        for row in reader:
            PRODUCTS_TO_WATCH.append(Product(row[0], float(row[1])))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', help="set mode [default\\loggertest]")
    args = parser.parse_args()

    load_dotenv(find_dotenv())

    if args.mode == 'loggertest':
        Logger.log('test', 'Logger has all required permissions')
    elif args.mode == 'dbtest':
        test_database()
    else:
        load_products()
        list(map(lambda product: watch(product.url, product.price), PRODUCTS_TO_WATCH))
