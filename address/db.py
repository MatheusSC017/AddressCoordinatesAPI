import pymongo
from flask import abort
from bson.objectid import ObjectId
from flask import current_app, g
from .utils import singleton


@singleton
class AddressDB:
    db = None
    _address_collection = None

    def get_db(self):
        if 'db' not in g:
            client = pymongo.MongoClient(
                current_app.config['DATABASE']
            )

            g.db = client['mongodbcoordinates']

        return g.db

    def close_db(self, e=None):
        db = g.pop('db', None)

        if db is not None:
            db.close()

    @property
    def address_collection(self):
        if self._address_collection is not None:
            return self._address_collection

        db = self.get_db()
        self._address_collection = db['address']
        return self._address_collection

    def get_address(self, address_id):
        address = self.address_collection.find_one({'_id': ObjectId(address_id)})

        if address is None:
            abort(404, 'Address not found')

        return address

    def get_addresses(self):
        return self.address_collection.find()

    def register_address(self, address):
        self.address_collection.insert_one(address)

    def update_address(self, address_id, address):
        self.address_collection.update_one({'_id': ObjectId(address_id)}, {'$set': address})

    def delete_address(self, address_id):
        self.address_collection.delete_one({'_id': ObjectId(address_id)})
