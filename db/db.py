'''db'''

import os
from webbrowser import get
from pymongo import MongoClient

_CONNECTION = None


def get_connection():
    '''init DB connection'''

    global _CONNECTION

    if not _CONNECTION:
        _CONNECTION = MongoClient(os.environ.get("DATABASE_URL"))
    return _CONNECTION


def get_db():
    '''get db'''

    return get_connection()[os.environ.get("DATABASE_NAME")]


__all__ = ['get_connection']
