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

        try:
            prod_title = self.soup.find(
                'h1', {"data-cy": "ad_title"}).get_text().strip()
        except BaseException:
            print('Couldn\'t find title for', self.url)

            self.mark_as_inactive()
            self.stop(send_email=True)

        try:
            price = self.soup.select(
                'div[data-testid="ad-price-container"] h3')[0].get_text()
        except BaseException:
            print('Couldn\'t find price for', prod_title)

        price = price.replace('zł', '').replace(' ', '')
        price_parsed = float(price)

        parse_time = datetime.datetime.now()

        db_product = ProductUtil.get_db_entity(
            {"product_id":  self.product_id})

        # TODO: extract to Watcher.py
        history_collection = db.get_db()['history']
        history_collection.insert_one({
            'product_id': self.product_id,
            'product_title': prod_title,
            'price_parsed': price_parsed,
            'price_threshold': db_product.get('threshold_price', None),
            'parse_time': parse_time
        })

        self.check_notify(price_parsed, prod_title)
