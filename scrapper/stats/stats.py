from const.options import CREATE_STATISTICS_INTERVAL
from db import db
from datetime import datetime
from utils.threading import set_interval
from pymongo import ASCENDING, DESCENDING

def create_statistics(once = False):
    def start():
        products = db.get_db()['products']
        history = db.get_db()['history']

        data = {}
        data['created_at'] = datetime.now()

        # products count
        data['count'] = products.count_documents({})

        # products avg price change 
        aggregated_change = 0
        products_count = 0

        for product in products.find({}):
            id = product.get('product_id', None)
            if not id:
                # very old product
                continue

            max_price_parsed_document = history.find({ 'product_id': id }).sort('price_parsed', DESCENDING).limit(1)
            max_document = next(max_price_parsed_document, None)

            min_price_parsed_document = history.find({ 'product_id': id }).sort('price_parsed', ASCENDING).limit(1)
            min_document = next(min_price_parsed_document, None)

            if max_document and min_document:
                change = float(min_document.get("price_parsed", None)) - float(max_document.get("price_parsed", None))

                # TODO: should handle different currencies somehow
                aggregated_change += change
                products_count += 1

        data['average_change'] = round(aggregated_change / products_count, 0)

        # working since
        first_scrap_ever = history.find_one()

        data['works_since'] = first_scrap_ever.get('parse_time', None)

        db.get_db()['statistics'].insert_one(data)
        print('[Stats] Created: ', data)

    start()

    if not once:
        set_interval(start, CREATE_STATISTICS_INTERVAL)
