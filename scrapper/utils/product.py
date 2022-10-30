from db import db

class ProductUtil(object):
    def get_current_price(product):
        return product.get('last_found_price', None) or product.get('price', None)

    def get_db_entity(filter):
        return db.get_db()['products'].find_one(filter)