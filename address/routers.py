from flask import (
    Blueprint, flash, request, request, Response
)
from flask_restful import Resource
from bson.json_util import dumps
from .utils import geocoding
from .validations import check_required_fields
from .db import AddressDB

address_db = AddressDB()


def initialize_routes(api):
    api.add_resource(AddressesApi, '/api/addresses')
    api.add_resource(AddressApi, '/api/address/<id>')


class AddressesApi(Resource):
    def get(self):
        addresses = address_db.get_addresses()
        return Response(dumps(addresses), mimetype='application/json', status=200)

    def post(self):
        fields = ['number', 'street', 'district', 'city', 'state', 'country', ]
        required_fields = fields[1:]

        address = {field: request.form.get(field, '') for field in fields}
        errors = check_required_fields(address, required_fields)

        if len(errors):
            return Response(dumps(errors), mimetype='application/json', status=400)
        else:
            address['location'] = {'type': 'Point', 'coordinates': geocoding(address)}
            address_db.register_address(address)

        return Response(dumps("Registration created successfully"), mimetype='application/json', status=200)


class AddressApi(Resource):
    def get(self, id):
        address = address_db.get_address(id)
        return Response(dumps(address), mimetype='application/json', status=200)

    def put(self, id):
        fields = ['number', 'street', 'district', 'city', 'state', 'country', ]
        required_fields = fields[1:]

        address = {field: request.form.get(field, '') for field in fields}
        print(address)
        errors = check_required_fields(address, required_fields)

        if len(errors):
            return Response(dumps(errors), mimetype='application/json', status=400)
        else:
            address_db.update_address(id, address)

        address = address_db.get_address(id)
        return Response(dumps(address), mimetype='application/json', status=200)

    def delete(self, id):
        address_db.delete_address(id)
        return Response(dumps("Registration deleted successfully"), mimetype='application/json', status=200)
