'''Otodom watcher module'''
import datetime
from utils.product import ProductUtil
from watchers.watcher import Watcher, NoElemFoundExcpetion
from db import db


class OtodomWatcher(Watcher):
    '''Otodom watcher'''

    def __init__(self, event, URL, price):
        Watcher.__init__(self, event, URL)
        print('[INFO] Starting OtoDom watcher:\n URL: ',
              URL, '\n Threshold price: ', price)

    def scrap(self):
        '''Do site-specific scrapping'''

        if self.product_id is None:
            self.product_id = self.url.rsplit('/', 1)[-1].replace('.html', '')
            self.add_product_id(product_id=self.product_id)

        try:
            prod_title = self.soup.find(
                "h1", {"data-cy": "adPageAdTitle"}).get_text().strip()
        except BaseException:
            print('Couldn\'t find title for', self.url)

            self.mark_as_inactive()
            self.stop(send_email=True)

        try:
            price = self.soup.find(
                "strong", {"data-cy": "adPageHeaderPrice"}).get_text()
        except BaseException:
            raise NoElemFoundExcpetion('Couldn\'t find price for', prod_title)

        price = price.replace('zł', '').replace(' ', '')
        price_parsed = float(price)

        parse_time = datetime.datetime.now()

        db_product = ProductUtil.get_db_entity({"url":  self.url})

        print('[', parse_time, ']', ' Otodom.pl: ',
              prod_title, ' : ', price_parsed, ' threshold: ', ProductUtil.get_current_price(db_product))

        history_collection = db.get_db()['history']
        history_collection.insert_one({
            'product_id': self.product_id,
            'product_title': prod_title,
            'price_parsed': price_parsed,
            'price_threshold': self.price,
            'parse_time': parse_time
        })

        self.send_if_fulfilled(price_parsed, prod_title)
