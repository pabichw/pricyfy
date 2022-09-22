'''Otodom watcher module'''
import datetime
from watchers.watcher import Watcher, NoElemFoundExcpetion
from db import db


class OtodomWatcher(Watcher):
    '''Otodom watcher'''

    def __init__(self, event, URL, price):
        Watcher.__init__(self, event, URL, price)
        print('[INFO] Starting OtoDom watcher:\n URL: ',
              URL, '\n Expected Price: ', price)

    def scrap(self):
        '''Do site-specific scrapping'''
        try:
            prod_title = self.soup.find(
                "h1", {"data-cy": "adPageAdTitle"}).get_text().strip()
        except BaseException:
            raise NoElemFoundExcpetion('Couldn\'t find title for', self.url)
        try:
            price = self.soup.find(
                "strong", {"data-cy": "adPageHeaderPrice"}).get_text()
        except BaseException:
            raise NoElemFoundExcpetion('Couldn\'t find price for', prod_title)

        price = price.replace('zł', '').replace(' ', '')
        price_parsed = float(price)

        parse_time = datetime.datetime.now()
        id = self.url.rsplit('/', 1)[-1].replace('.html', '')

        print('[', parse_time, ']', ' Otodom.pl: ',
              prod_title, ' : ', price_parsed, ' threshold: ', self.price)

        history_collection = db.get_db()['history']
        history_collection.insert_one({
            'product_id': id,
            'product_title': prod_title,
            'price_parsed': price_parsed,
            'price_threshold': self.price,
            'parse_time': parse_time
        })

        self.send_if_fulfilled(price_parsed, prod_title)
