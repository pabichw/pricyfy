from watchers.watcher import Watcher


class MediaExpertWatcher(Watcher):
    def __init__(self, event, URL, price):
        Watcher.__init__(self, event, URL, price)
        print(f'[INFO] Starting MediaExpert watcher:\n URL: {URL}\n Price: {price}', )

    def scrap(self):
        prod_title = self.soup.find(id='p-inner-name').get_text().strip()
        price = self.soup.findAll('span', {'class': 'price'}).get_text()

        price = price.replace('\xa0€', '').replace(',', '.')
        price_parsed = float(price)

        self.sendIfFulfilled(price_parsed, prod_title)
