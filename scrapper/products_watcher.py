'''main watcher module'''
from threading import Thread, Event
from os import environ
import csv
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv, find_dotenv

from const.shops_domains import ShopDomains
from const.options import QUEUE_BROWSING_INTERVAL
from models.product import Product
from utils.sender import EmailTemplates, Sender
from watchers.watcher import Watcher
from watchers.amazon_watcher import AmazonWatcher
from watchers.media_expert_watcher import MediaExpertWatcher
from watchers.otodom_watcher import OtodomWatcher
from watchers.olx_watcher import OlxWatcher
from utils.logger import Logger
from db import db
from utils.threading import set_interval
from stats.stats import create_statistics
from utils.product import ProductUtil

PRODUCTS_TO_WATCH = []


def watch(url):
    '''run watch process for each product'''

    stop_flag = Event()
    domain = urlparse(url).netloc

    thread_handler = Thread()

    if domain == ShopDomains.AMAZON:
        thread_handler = AmazonWatcher(stop_flag, url)
    elif domain == ShopDomains.MEDIA_EXPERT:
        thread_handler = MediaExpertWatcher(stop_flag, url)
    elif domain == ShopDomains.OTO_DOM:
        thread_handler = OtodomWatcher(stop_flag, url)
    elif domain == ShopDomains.OLX:
        thread_handler = OlxWatcher(stop_flag, url)
    elif domain == ShopDomains.M_OLX:
        thread_handler = OlxWatcher(stop_flag, url)
    # elif domain == SHOPS_DOMAINS.KOMPUTRONIK:
        # threadHandler = KomputronikWatcher(stop_flag, URL, price)
    else:
        print('[WARN] Platform not supported: ', domain)
        return
    thread_handler.start()


def watch_products_queue():
    def start():
        print('[Queue] Browsing queue...')
        productsQueue = db.get_db()['products_queue'].find({})

        for waiting_product in productsQueue:
            print(f"-- Adding: {waiting_product['url']}")

            product_id = Watcher.create_id(waiting_product['url'])

            if db.get_db()['products'].count_documents({'product_id': product_id}) != 0:
                print( f'Product already exists {product_id} Simply adding recipients: {waiting_product["recipients"]}')
                # TODO: handle email already a recipient and Product exists but INACTIVE

                db.get_db()['products'].update_one({"product_id": product_id}, { "$push": {'recipients': {'$each': waiting_product['recipients']}}})
            else:
                db.get_db()['products'].insert_one({ 'url': waiting_product['url'], 'recipients': waiting_product['recipients'], 'status': 'JUST_ADDED' })
                watch(waiting_product['url'])

            db.get_db()['products_queue'].delete_one({ 'url': waiting_product['url'] })
            
            Sender.send_mail(
                variables={
                    'url': waiting_product['url']
                },
                to=waiting_product['recipients'],
                type=EmailTemplates.WATCH_STARTED)
    start()
    set_interval(start, QUEUE_BROWSING_INTERVAL)

def test_database():
    '''test database connection'''

    test_collection = db.get_db()['test']
    insert = test_collection.insert_one({"foo": "bar"})

    print('---- DB test ----')
    print('Insert:', bool(insert))


def test_email():
    '''test email sender'''

    email = environ.get('DEV_EMAIL')

    print('---- Email sender test ----')
    print(f'Sending to {email}...')
    Sender.send_mail(to=[email], type=EmailTemplates.TEST)

def test_statistics():
    '''test statistics creation'''

    create_statistics(once = True)

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
    products_all = products_collection.find({ "status": { "$ne": "INACTIVE" } })

    for document in products_all:
        PRODUCTS_TO_WATCH.append(
            Product(document['url'], ProductUtil.get_current_price(document)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument( '-m', '--mode', help="set mode [default\\loggertest\\emailtest\\dbtest\\statstest]")
    args = parser.parse_args()

    load_dotenv(find_dotenv())

    if args.mode == 'loggertest':
        Logger.log('test', 'Logger has all required permissions')
    elif args.mode == 'dbtest':
        test_database()
    elif args.mode == 'emailtest':
        test_email()
    elif args.mode == 'statstest':
        test_statistics()
    else:
        load_products()
        list(map(lambda product: watch(product.url), PRODUCTS_TO_WATCH))

        watch_products_queue()
        create_statistics()
