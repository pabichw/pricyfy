import datetime
from watchers.watcher import Watcher, NoElemFoundExcpetion
from utils.logger import Logger

class OtodomWatcher(Watcher):
    def __init__(self, event, URL, price):
        Watcher.__init__(self, event, URL, price)
        print('[INFO] Starting OtoDom watcher:\n URL: ', URL,'\n Expected Price: ', price)

    def scrap(self):
        try:
            prod_title = self.soup.find("h1", {"data-cy":"adPageAdTitle"}).get_text().strip()
        except:
           raise NoElemFoundExcpetion('Couldn\'t find title for', self.URL)
        try:
            price = self.soup.find("strong", {"data-cy":"adPageHeaderPrice"}).get_text()
        except:
           raise NoElemFoundExcpetion('Couldn\'t find price for', prod_title)

        price = price.replace('zł', '').replace(' ', '')
        price_parsed = float(price)

        print('[', datetime.datetime.now(), ']', ' Otodom.pl: ', prod_title, ' : ', price_parsed, ' need: ', self.price)
        Logger.log(self.URL.rsplit('/', 1)[-1], f'{datetime.datetime.now()},{price_parsed}\n')

        self.sendIfFulfilled(price_parsed, prod_title)
