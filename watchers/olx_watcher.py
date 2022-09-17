'''Olx watcher module'''
import datetime
from watchers.watcher import Watcher, NoElemFoundExcpetion
from utils.logger import Logger


class OlxWatcher(Watcher):
    '''Olx watcher'''

    def __init__(self, event, URL, price):
        Watcher.__init__(self, event, URL, price)
        print('[INFO] Starting OtoDom watcher:\n URL: ',
              URL, '\n Expected Price: ', price)

    def scrap(self):
        '''Do site-specific scrapping'''
        try:
            prod_title = self.soup.find(
                'h1', {"data-cy": "ad_title"}).get_text().strip()
        except BaseException:
            raise NoElemFoundExcpetion('Couldn\'t find title for', self.url)

        try:
            price = self.soup.select(
                'div[data-testid="ad-price-container"] h3')[0].get_text()
        except BaseException:
            raise NoElemFoundExcpetion('Couldn\'t find price for', prod_title)

        print('price ', price)
        price = price.replace('zł', '').replace(' ', '')
        price_parsed = float(price)

        print('price_parsed', price_parsed)
        print('prod_title', prod_title)

        print('[', datetime.datetime.now(), ']', ' Olx.pl: ',
              prod_title, ' : ', price_parsed, ' need: ', self.price)
        Logger.log(
            self.url.rsplit('/', 1)[-1].replace('.html', ''),
            f'{datetime.datetime.now()},{price_parsed}\n')

        self.send_if_fulfilled(price_parsed, prod_title)
