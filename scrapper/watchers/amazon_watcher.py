'''Amazon watcher module'''
import datetime
from watchers.watcher import Watcher, NoElemFoundExcpetion


class AmazonWatcher(Watcher):
    '''Amazon watcher'''

    def __init__(self, event, URL, price):
        Watcher.__init__(self, event, URL, price)
        print('[INFO] Starting amazon watcher:\n URL: ',
              URL, '\n Threshold price: ', price)

    def scrap(self):
        '''Do site-specific scrapping'''
        try:
            prod_title = self.soup.find(id='productTitle').get_text().strip()
        except BaseException:
            raise NoElemFoundExcpetion('Couldn\'t find title for', self.url)
        try:
            price = self.soup.find(id='priceblock_ourprice').get_text()
        except BaseException:
            raise NoElemFoundExcpetion('Couldn\'t find price for', prod_title)

        # TODO: need exact element ID ;(
        # try:
        #    additional_discount = self.soup.find(id='priceblock_ourprice').get_text()
        # except:
        #   raise NoElemFoundExcpetion('No additional discount found for', prod_title)

        price = price.replace('\xa0€', '').replace(',', '.')
        price_parsed = float(price)

        print('[', datetime.datetime.now(), ']', ' Amazon.de: ',
              prod_title, ' : ', price_parsed, ' need: ', self.price)
        self.check_notify(price_parsed, prod_title)
