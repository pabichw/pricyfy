'''Olx watcher module'''
import datetime
from watchers.watcher import Watcher, NoElemFoundExcpetion
from db import db
from utils.product import ProductUtil


class OlxWatcher(Watcher):
    '''Olx watcher'''

    title = 'OLX'

    def __init__(self, event, URL, price):
        Watcher.__init__(self, event, URL)
        print('[INFO] Starting Olx watcher:\n URL: ',
              URL, '\n Threshold price: ', price)

    def scrap(self):
        '''Do site-specific scrapping'''

        super().scrap()

        # TODO: extract collect data?
        try:
            prod_title = self.soup.find(
                'h1', {"data-cy": "ad_title"}).get_text().strip()
        except BaseException:
            print(f'Couldn\'t find title for {self.url}')
            self.mark_as_inactive()
            self.stop(send_email=True)

        try:
            price = self.soup.select(
                'div[data-testid="ad-price-container"] h3')[0].get_text()
        except BaseException:
            print(f'Couldn\'t find price for {self.url}')

        price = price.replace('zł', '').replace(' ', '')
        price_parsed = float(price)

        db_product = ProductUtil.get_db_entity(
            {"product_id":  self.product_id})

        # TODO: extract to Watcher.py
        history_collection = db.get_db()['history']
        history_collection.insert_one({
            'product_id': self.product_id,
            'product_title': prod_title,
            'price_parsed': price_parsed,
            'price_threshold': db_product.get('threshold_price', None),
            'parse_time': datetime.datetime.now()
        })

        self.check_notify(price_parsed, prod_title)

    def collect_images(self):
        print('Collecting images...')
        super().scrap()

        try:
            images = self.soup.select(
                'div[data-cy="adPhotos-swiperSlide"] img')

            if images:
                srcs = list(map(
                    lambda img: img.get('src') or img.get('data-src'), images))

                db.get_db()['products'].update_one(
                    {"product_id": self.product_id},
                    {"$set": {'images': srcs}})
        except BaseException:
            print(f'Couldn\'t find images for {self.url}')
