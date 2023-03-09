import pymongo
from flask import current_app, g


def get_db():
    if 'db' not in g:
        client = pymongo.MongoClient(
            current_app.config['DATABASE']
        )

        g.db = client['mongodbcoordinates']

    return g.db


def get_address_collection():
    db = get_db()
    address_collection = db['address']

    return address_collection


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
