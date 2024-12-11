'''Otodom watcher module'''
import datetime
from utils.logger import Logger
from utils.product import ProductUtil
from watchers.watcher import Watcher, NoElemFoundExcpetion
from db import db
import json


class OtodomWatcher(Watcher):
    '''Otodom watcher'''

    title = "OtoDom"

    def __init__(self, event, URL):
        Watcher.__init__(self, event, URL)
        
        db_product = ProductUtil.get_db_entity({"product_id":  self.product_id})

        print(f'[INFO] Starting OtoDom watcher:\n URL: {URL} \nPrice: {ProductUtil.get_current_price(db_product)}')
        
    def scrap(self, initial=False):
        '''Do site-specific scrapping'''

        super().scrap()

        try:
            prod_title = self.soup.find("h1", {"data-cy": "adPageAdTitle"}).get_text().strip()
        except BaseException:
            self.mark_as_inactive()
            self.stop(send_email=True)
            print('Couldn\'t find title for', self.url)
            return

        price = ''
        try:
            price = self.soup.find("strong", {"data-cy": "adPageHeaderPrice"}).get_text()
        except BaseException:
            raise NoElemFoundExcpetion('Couldn\'t find price for', self.url)

        price = price.replace('zł', '').replace(' ', '')
        price_parsed = float(price)

        parse_time = datetime.datetime.now()

        history_collection = db.get_db()['history']
        history_collection.insert_one({
            'product_id': self.product_id,
            'product_title': prod_title,
            'price_parsed': price_parsed,
            'parse_time': parse_time
        })

        if not initial: 
            self.check_notify(price_parsed, prod_title)

        self.update_last_price(price_parsed)

    def collect_images(self):
        print('Collecting images...')

        try:
            next_script = self.soup.find('script', {'id': '__NEXT_DATA__'})
            site_json = json.loads(next_script.string)
            images = site_json['props']['pageProps']['ad']['images']

            if images:
                srcs = list(map(
                    lambda img: img.get("medium"), images))

                db.get_db()['products'].update_one(
                    {"product_id": self.product_id},
                    {"$set": {'images': srcs}})
        except BaseException as e:
            print(f'Couldn\'t find images for {self.url}')
            print(f'Error: {e}')
