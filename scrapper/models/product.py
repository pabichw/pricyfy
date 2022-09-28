'''module product model'''


class Product:
    '''product model'''

    url = ''
    price = 0

    def __init__(self, url, price):
        self.url = url
        self.price = price
