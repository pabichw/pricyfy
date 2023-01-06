from const.options import CREATE_STATISTICS_INTERVAL
from db import db
from datetime import datetime
from utils.threading import set_interval

def create_statistics():
    def start():
        products = db.get_db()['products']

        data = {}
        data['created_at'] = datetime.now()

        # products count
        data['count'] = products.count_documents({})

        db.get_db()['statistics'].insert_one(data)

        print('[Stats] Created: ', data)

    start()
    set_interval(start, CREATE_STATISTICS_INTERVAL)
