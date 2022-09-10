import datetime
from watchers.watcher import Watcher, NoElemFoundExcpetion

class AmazonWatcher(Watcher):
    def __init__(self, event, URL, price):
        Watcher.__init__(self, event, URL, price)
        print('[INFO] Starting amazon watcher:\n URL: ', URL,'\n Expected Price: ', price)

    def scrap(self):
        try:
            prod_title = self.soup.find(id='productTitle').get_text().strip()
        except:
           raise NoElemFoundExcpetion('Couldn\'t find title for', self.URL)
        try:
            price = self.soup.find(id='priceblock_ourprice').get_text()
        except:
           raise NoElemFoundExcpetion('Couldn\'t find price for', prod_title)

        #TODO: need exact element ID ;(
        #try:
        #    additional_discount = self.soup.find(id='priceblock_ourprice').get_text()
        #except:
        #   raise NoElemFoundExcpetion('No additional discount found for', prod_title)

        price = price.replace('\xa0€', '').replace(',', '.')
        price_parsed = float(price)

        print('[', datetime.datetime.now(), ']', ' Amazon.de: ', prod_title, ' : ', price_parsed, ' need: ', self.price)
        self.sendIfFulfilled(price_parsed, prod_title)
