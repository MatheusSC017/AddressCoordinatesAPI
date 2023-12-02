from flask import request, Response
from flask_restful import Resource
from bson.json_util import dumps
from .utils import geocoding, haversine_distance, validate_coordinates
from .validations import validate_required_fields
from .db import AddressDB

address_db = AddressDB()


def initialize_routes(api):
    api.add_resource(AddressesApi, '/api/addresses')
    api.add_resource(AddressApi, '/api/address/<id>')
    api.add_resource(ClosestDistanceApi, '/api/distance/closest')
    api.add_resource(AddressesDistanceApi, '/api/distance/addresses')
    api.add_resource(RegisteredAddressDistanceApi, '/api/distance/registers')


class AddressesApi(Resource):
    def get(self):
        addresses = address_db.get_addresses()
        return Response(dumps(addresses), mimetype='application/json', status=200)

    def post(self):
        try:
            fields = ['number', 'street', 'district', 'city', 'state', 'country', ]
            required_fields = fields[1:]

            address = {field: request.form.get(field) for field in fields if request.form.get(field)}
            validate_required_fields(address, required_fields)

            address['location'] = {'type': 'Point', 'coordinates': geocoding(address)}
            address_db.register_address(address)

            return Response(dumps("Registration created successfully"), mimetype='application/json', status=200)
        except ValueError as e:
            return Response(dumps(f"Invalid parameter value: {str(e)}"), mimetype='application/json', status=400)
        except Exception as e:
            return Response(dumps(f"An error has occurred: {str(e)}"), mimetype='application/json', status=400)


class AddressApi(Resource):
    def get(self, id):
        try:
            address = address_db.get_address(id)
            return Response(dumps(address), mimetype='application/json', status=200)
        except Exception as e:
            return Response(dumps(f"An error has occurred: {str(e)}"), mimetype='application/json', status=404)


    def put(self, id):
        try:
            fields = ['number', 'street', 'district', 'city', 'state', 'country', ]
            required_fields = fields[1:]

            address = {field: request.form.get(field) for field in fields if request.form.get(field)}
            validate_required_fields(address, required_fields)

            address['location'] = {'type': 'Point', 'coordinates': geocoding(address)}
            address_db.update_address(id, address)

            address = address_db.get_address(id)
            return Response(dumps(address), mimetype='application/json', status=200)
        except ValueError as e:
            return Response(dumps(f"Invalid parameter value: {str(e)}"), mimetype='application/json', status=400)
        except Exception as e:
            return Response(dumps(f"An error has occurred: {str(e)}"), mimetype='application/json', status=400)

    def delete(self, id):
        try:
            address_db.delete_address(id)
            return Response(dumps("Registration deleted successfully"), mimetype='application/json', status=200)
        except Exception as e:
            return Response(dumps(f"An error has occurred: {str(e)}"), mimetype='application/json', status=404)


class ClosestDistanceApi(Resource):
    def get(self):
        try:
            coordinates = [float(request.args.get('lat')), float(request.args.get('lng'))]
            validate_coordinates(coordinates)
            nearest_address = address_db.get_nearest_establishment(coordinates)
            return Response(dumps(nearest_address), mimetype='application/json', status=200)
        except ValueError as e:
            return Response(dumps(f"Invalid parameter value: {str(e)}"), mimetype='application/json', status=400)
        except Exception as e:
            return Response(dumps(f"An error has occurred: {str(e)}"), mimetype='application/json', status=400)


class AddressesDistanceApi(Resource):
    def get(self):
        try:
            addresses = request.get_json()
            start_coordinates = geocoding(addresses['start_address'])
            end_coordinates = geocoding(addresses['end_address'])
            distance = haversine_distance(start_coordinates, end_coordinates)
            return Response(dumps(distance), mimetype='application/json', status=200)
        except Exception as e:
            return Response(dumps(f"An error has occurred: {str(e)}"), mimetype='application/json', status=400)


class RegisteredAddressDistanceApi(Resource):
    def get(self):
        try:
            start_coordinates = address_db.get_address(request.args.get('start_id_address'))['location']['coordinates']
            end_coordinates = address_db.get_address(request.args.get('end_id_address'))['location']['coordinates']
            distance = haversine_distance(start_coordinates, end_coordinates)
            return Response(dumps(distance), mimetype='application/json', status=200)
        except Exception as e:
            return Response(dumps(f"An error has occurred: {str(e)}"), mimetype='application/json', status=400)
