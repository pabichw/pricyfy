'''main watcher module'''
from threading import Thread, Event, Timer
import csv
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv, find_dotenv

from const.shops_domains import ShopDomains
from const.options import QUEUE_BROWSING_INTERVAL
from models.product import Product
from watchers.amazon_watcher import AmazonWatcher
from watchers.media_expert_watcher import MediaExpertWatcher
from watchers.otodom_watcher import OtodomWatcher
from watchers.olx_watcher import OlxWatcher
from utils.logger import Logger
from db import db

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


def watch_products_queue():
    def start():
        print('[Queue] Browsing queue...')
        productsQueue = db.get_db()['products_queue'].find({})

        for waiting_product in productsQueue:
            print(
                f"-- Adding: {waiting_product['url']} : {waiting_product['threshold_price']} : {waiting_product['threshold_price']}")

            # TODO: update if exists (also handle if email exists)

            db.get_db()['products'].insert_one(
                {'url': waiting_product['url'], 'threshold_price': waiting_product['threshold_price'], 'recipients': waiting_product['recipients']})

            watch(waiting_product['url'], waiting_product['threshold_price'])

            db.get_db()['products_queue'].delete_one(
                {'url': waiting_product['url'], 'threshold_price': waiting_product['threshold_price']})

    start()

    t = Timer(QUEUE_BROWSING_INTERVAL, start)
    t.start()
    return t


def test_database():
    '''test database connection'''

    test_collection = db.get_db()['test']
    insert = test_collection.insert_one({"foo": "bar"})

    print('---- DB test ----')
    print('Insert:', bool(insert))


def load_products_from_csv():
    '''load products from csv'''

    print('[INFO] Loading products from csv...')

    with open('products.csv', newline='') as products_csv:
        reader = csv.reader(products_csv, delimiter=' ', quotechar='|')
        for row in reader:
            PRODUCTS_TO_WATCH.append(Product(row[0], float(row[1])))


def load_products():
    '''load products from db'''

    global PRODUCTS_TO_WATCH

    print('[INFO] Loading products from DB...')

    products_collection = db.get_db()['products']
    products_all = products_collection.find({})

    for document in products_all:
        print(document)
        PRODUCTS_TO_WATCH.append(
            Product(document['url'], document['threshold_price']))


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
        list(map(lambda product: watch(
            product.url,
            db.get_db()['products'].find_one({'url': product.url}).get('last_found_price', None) or product.price), PRODUCTS_TO_WATCH))

        watch_products_queue()
