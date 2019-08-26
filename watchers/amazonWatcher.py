import datetime
from watchers.watcher import Watcher


class AmazonWatcher(Watcher):
    def __init__(self, event, URL, price):
        Watcher.__init__(self, event, URL, price)
        print(f'[INFO] Starting amazon watcher:\n URL: {URL}\n Price: {price}', )

    def scrap(self):
        prod_title = self.soup.find(id='productTitle').get_text().strip()
        price = self.soup.find(id='priceblock_ourprice').get_text()

        price = price.replace('\xa0€', '').replace(',', '.')
        price_parsed = float(price)

        self.sendIfFulfilled(price_parsed, prod_title)
