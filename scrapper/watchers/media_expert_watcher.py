'''MediaExpert watcher module'''
import datetime
from watchers.watcher import Watcher


class MediaExpertWatcher(Watcher):
    '''MediaExpert watcher'''

    def __init__(self, event, URL, price):
        Watcher.__init__(self, event, URL, price)
        print('[INFO] Starting MediaExpert watcher:\n URL: ',
              URL, '\n Threshold price:', price)

    def scrap(self):
        '''Do site-specific scrapping'''
        prod_title = self.soup.find(id='p-inner-name').get_text().strip()
        price = self.soup.findAll('span', {'class': 'price'}).get_text()

        price = price.replace('\xa0€', '').replace(',', '.')
        price_parsed = float(price)

        print('[', datetime.datetime.now(), ']', ' MediaExpert ',
              prod_title, ' : ', price_parsed, ' need: ', self.price)
        self.check_notify(price_parsed, prod_title)
