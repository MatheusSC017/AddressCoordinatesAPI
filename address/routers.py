from flask import (
    Blueprint, flash, request, request, Response
)
from flask_restful import Resource
from bson.json_util import dumps
from .utils import geocoding, haversine_distance
from .validations import check_required_fields
from .db import AddressDB

address_db = AddressDB()


def initialize_routes(api):
    api.add_resource(AddressesApi, '/api/addresses')
    api.add_resource(AddressApi, '/api/address/<id>')
    api.add_resource(DistanceApi, '/api/distance')


class AddressesApi(Resource):
    def get(self):
        addresses = address_db.get_addresses()
        return Response(dumps(addresses), mimetype='application/json', status=200)

    def post(self):
        fields = ['number', 'street', 'district', 'city', 'state', 'country', ]
        required_fields = fields[1:]

        address = {field: request.form.get(field) for field in fields if request.form.get(field)}
        print(address)
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

        address = {field: request.form.get(field) for field in fields if request.form.get(field)}
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


class DistanceApi(Resource):
    def get(self):
        if 'lat' in request.args.keys() and 'lng' in request.args.keys():
            coordinates = [float(request.args.get('lat')), float(request.args.get('lng'))]
            nearest_address = address_db.get_nearest_establishment(coordinates)
            return Response(dumps(nearest_address), mimetype='application/json', status=200)
        elif request.content_type:
            coordinates = request.get_json()
            start_coordinates = geocoding(coordinates['start_address'])
            end_coordinates = geocoding(coordinates['end_address'])
            distance = haversine_distance(start_coordinates, end_coordinates)
            return Response(dumps(distance), mimetype='application/json', status=200)
        elif 'start_id_address' in request.args.keys() and 'end_id_address' in request.args.keys():
            start_coordinates = address_db.get_address(request.args.get('start_id_address'))['location']['coordinates']
            end_coordinates = address_db.get_address(request.args.get('end_id_address'))['location']['coordinates']
            distance = haversine_distance(start_coordinates, end_coordinates)
            return Response(dumps(distance), mimetype='application/json', status=200)

        return Response(dumps("No search parameters were provided"), mimetype='application/json', status=400)
