import pymongo
from bson.objectid import ObjectId
from flask import current_app, g
from flask_pymongo import PyMongo
from .utils import singleton


class MongoDB:
    _collection_name = None
    _collection = None
    mongodb = None

    def get_db(self):
        if 'db' not in g:
            self.mongodb = PyMongo(current_app)
            g.db = self.mongodb.db

        return g.db

    def close_db(self, e=None):
        db = g.pop('db', None)

        if db is not None:
            db.close()

    @property
    def collection(self):
        if self._collection is not None:
            return self._collection

        db = self.get_db()
        self._collection = db[self._collection_name]
        return self._collection


@singleton
class AddressDB(MongoDB):
    _collection_name = 'address'

    @property
    def collection(self):
        if self._collection is not None:
            return self._collection

        db = self.get_db()
        db[self._collection_name].create_index([("location", pymongo.GEOSPHERE)])
        self._collection = db[self._collection_name]
        return self._collection

    def get_address(self, address_id):
        address = self.collection.find_one({'_id': ObjectId(address_id)})

        if address is None:
            raise Exception("Address not found")

        return address

    def get_addresses(self):
        return self.collection.find()

    def register_address(self, address):
        result = self.collection.insert_one(address)
        return result.inserted_id

    def update_address(self, address_id, address):
        self.collection.update_one({'_id': ObjectId(address_id)}, {'$set': address})

    def delete_address(self, address_id):
        result = self.collection.delete_one({'_id': ObjectId(address_id)})
        if result.deleted_count == 0:
            raise Exception("Error deleting or non-existing record")

    def get_nearest_establishment(self, coordinates):
        aggregation = [
            {'$geoNear': {
                'near': {'type': 'Point', 'coordinates': coordinates},
                'distanceField': 'distance',
                'query': {},
                'spherical': True}},
            {'$sort': {'distance': 1}},
            {'$limit': 1}
        ]
        return self.collection.aggregate(aggregation)


@singleton
class UserDB(MongoDB):
    _collection_name = 'users'

    def get_user(self, user_id):
        user = self.collection.find_one({'_id': ObjectId(user_id)})
        return user
