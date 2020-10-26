from threading import Thread, Event
import csv
from urllib.parse import urlparse
from const.shopsDomains import ShopsDomains
from models.product import Product
from watchers.amazonWatcher import AmazonWatcher
from watchers.mediaExpertWatcher import MediaExpertWatcher

PRODUCTS_TO_WATCH = []

def watch(URL, price):
    stop_flag = Event()
    domain = urlparse(URL).netloc

    threadHandler = Thread()
    if domain == ShopsDomains.AMAZON:
        threadHandler = AmazonWatcher(stop_flag, URL, price)
    elif domain == ShopsDomains.MEDIA_EXPERT:
        threadHandler = MediaExpertWatcher(stop_flag, URL, price)
    # elif domain == SHOPS_DOMAINS.KOMPUTRONIK:
        # threadHandler = KomputronikWatcher(stop_flag, URL, price)
    else:
        print('Shop not supported: ', domain)
        return
    threadHandler.start()

def loadProducts():
    print('[INFO] Loading products...')
    with open('products.csv', newline='') as products_csv:
        reader = csv.reader(products_csv, delimiter=' ', quotechar='|')
        for row in reader:
            PRODUCTS_TO_WATCH.append(Product(row[0], float(row[1])))

if __name__ == "__main__":
    loadProducts()
    list(map(lambda product: watch(product.url, product.price), PRODUCTS_TO_WATCH))
