import pymongo
from flask import abort
from bson.objectid import ObjectId
from flask import current_app, g


def get_db():
    if 'db' not in g:
        client = pymongo.MongoClient(
            current_app.config['DATABASE']
        )

        g.db = client['mongodbcoordinates']

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def get_address_collection():
    db = get_db()

    return db['address']


def get_address(address_id):
    address_collection = get_address_collection()
    address = address_collection.find_one({'_id': ObjectId(address_id)})

    if address is None:
        abort(404, 'Address not found')

    return address


def get_addresses():
    address_collection = get_address_collection()
    return address_collection.find()


def register_address(address):
    address_collection = get_address_collection()
    address_collection.insert_one(address)


def update_address(address_id, address):
    address_collection = get_address_collection()
    address_collection.update_one({'_id': ObjectId(address_id)}, {'$set': address})


def delete_address(address_id):
    address_collection = get_address_collection()
    address_collection.delete_one({'_id': ObjectId(address_id)})
