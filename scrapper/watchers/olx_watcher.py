'''Olx watcher module'''
import datetime
from watchers.watcher import Watcher, NoElemFoundExcpetion
from db import db
from utils.product import ProductUtil
from utils.logger import Logger


class OlxWatcher(Watcher):
    '''Olx watcher'''

    title = 'OLX'

    def __init__(self, event, URL):
        Watcher.__init__(self, event, URL)
        
        db_product = ProductUtil.get_db_entity({ "product_id":  self.product_id })
        print('[INFO] Starting Olx watcher:\n URL: ', URL, ' initial price: ', ProductUtil.get_current_price(db_product))

    def scrap(self, initial=False):
        '''Do site-specific scrapping'''

        super().scrap()

        # TODO: extract collect data?
        try:
            prod_title = self.soup.find('h1', {"data-cy": "ad_title"}).get_text().strip()
        except BaseException:
            Logger.log(f'ERR-SCRAP-{datetime.datetime.now()}-{self.product_id}', self.soup, 'html')
            self.mark_as_inactive()
            self.stop(send_email=True)
            print(f'Couldn\'t find title for {self.url}')
            return

        price = ''
        try:
            price = self.soup.select('div[data-testid="ad-price-container"] h3')[0].get_text()
        except BaseException:
            raise NoElemFoundExcpetion(f'Couldn\'t find price for {self.url}')

        price = price.replace('zł', '').replace(' ', '')
        price_parsed = float(price)

        # TODO: extract to Watcher.py
        history_collection = db.get_db()['history']
        history_collection.insert_one({
            'product_id': self.product_id,
            'product_title': prod_title,
            'price_parsed': price_parsed,
            'parse_time': datetime.datetime.now()
        })
        
        if not initial:
            self.check_notify(price_parsed, prod_title)
        
        self.update_last_price(price_parsed)

    def collect_images(self):
        print('Collecting images...')

        try:
            images = self.soup.select('div[data-cy="adPhotos-swiperSlide"] img')

            if images:
                srcs = list(map(lambda img: img.get('src') or img.get('data-src'), images))

                db.get_db()['products'].update_one(
                    {"product_id": self.product_id},
                    {"$set": {'images': srcs}})

        except BaseException:
            print(f'Couldn\'t find images for {self.url}')
