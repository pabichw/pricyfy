'''Otodom watcher module'''
import datetime
from watchers.watcher import Watcher, NoElemFoundExcpetion
from utils.logger import Logger


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

        print('[', datetime.datetime.now(), ']', ' Otodom.pl: ',
              prod_title, ' : ', price_parsed, ' need: ', self.price)
        Logger.log(
            self.url.rsplit('/', 1)[-1],
            f'{datetime.datetime.now()},{price_parsed}\n')

        self.send_if_fulfilled(price_parsed, prod_title)
