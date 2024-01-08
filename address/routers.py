from flask import request, Response
from flask_restful import Resource
from bson.json_util import dumps
from .utils import geocoding, haversine_distance, validate_coordinates
from .validations import validate_required_fields
from .db import AddressDB
from .security import token_required
import requests
import json

address_db = AddressDB()

fields = ['complement', 'cep', 'number', 'street', 'district', 'city', 'state', 'country', ]
required_fields = fields[3:]


def initialize_routes(api):
    api.add_resource(AddressesApi, '/v1/addresses')
    api.add_resource(AddressApi, '/v1/address/<id>')
    api.add_resource(ClosestDistanceApi, '/v1/distance/closest')
    api.add_resource(AddressesDistanceApi, '/v1/distance/addresses')
    api.add_resource(RegisteredAddressDistanceApi, '/v1/distance/registers')


class AddressesApi(Resource):
    @token_required
    def get(self):
        addresses = address_db.get_addresses()
        return Response(dumps(addresses), mimetype='application/json', status=200)

    @token_required
    def post(self):
        try:
            address = {field: request.form.get(field) for field in fields if request.form.get(field)}
            validate_required_fields(address, required_fields)

            address['location'] = {'type': 'Point', 'coordinates': geocoding(address)}
            address_id = address_db.register_address(address)
            return Response(dumps({"address_id": str(address_id)}), mimetype='application/json', status=200)
        except ValueError as e:
            return Response(dumps({"error": f"Invalid parameter value: {str(e)}"}), mimetype='application/json', status=400)
        except Exception as e:
            return Response(dumps({"error": f"An error has occurred: {str(e)}"}), mimetype='application/json', status=400)


class AddressApi(Resource):
    @token_required
    def get(self, id):
        try:
            address = address_db.get_address(id)
            return Response(dumps(address), mimetype='application/json', status=200)
        except Exception as e:
            return Response(dumps({"error": f"An error has occurred: {str(e)}"}), mimetype='application/json', status=404)

    @token_required
    def put(self, id):
        try:
            address = {field: request.form.get(field) for field in fields if request.form.get(field)}
            validate_required_fields(address, required_fields)

            address['location'] = {'type': 'Point', 'coordinates': geocoding(address)}
            address_db.update_address(id, address)

            address = address_db.get_address(id)
            return Response(dumps(address), mimetype='application/json', status=200)
        except ValueError as e:
            return Response(dumps({"error": f"Invalid parameter value: {str(e)}"}), mimetype='application/json', status=400)
        except Exception as e:
            return Response(dumps({"error": f"An error has occurred: {str(e)}"}), mimetype='application/json', status=400)

    @token_required
    def delete(self, id):
        try:
            address_db.delete_address(id)
            return Response(dumps({"successful": "Registration deleted successfully"}), mimetype='application/json', status=200)
        except Exception as e:
            return Response(dumps({"error": f"An error has occurred: {str(e)}"}), mimetype='application/json', status=404)


class ClosestDistanceApi(Resource):
    @token_required
    def get(self):
        try:
            coordinates = [float(request.args.get('lat')), float(request.args.get('lng'))]
            validate_coordinates(coordinates)
            nearest_address = address_db.get_nearest_establishment(coordinates)
            return Response(dumps({"distance": nearest_address}), mimetype='application/json', status=200)
        except Exception as e:
            return Response(dumps({"error": f"An error has occurred: {str(e)}"}), mimetype='application/json', status=400)


class AddressesDistanceApi(Resource):
    @token_required
    def get(self):
        try:
            start_coordinates = geocoding(json.loads(request.args.get('start_address')))
            end_coordinates = geocoding(json.loads(request.args.get('end_address')))
            distance = haversine_distance(start_coordinates, end_coordinates)
            return Response(dumps({"distance": distance}), mimetype='application/json', status=200)
        except requests.exceptions.RequestException as e:
            return Response(dumps({"error": e}), mimetype='application/json', status=400)
        except Exception as e:
            return Response(dumps({"error": f"An error has occurred: {str(e)}"}), mimetype='application/json', status=400)


class RegisteredAddressDistanceApi(Resource):
    @token_required
    def get(self):
        try:
            start_address_id = request.args.get('start_id_address')
            end_id_address = request.args.get('end_id_address')
            if not start_address_id or not end_id_address:
                raise Exception("start_id_address and end_id_address are required")

            start_coordinates = address_db.get_address(start_address_id)['location']['coordinates']
            end_coordinates = address_db.get_address(end_id_address)['location']['coordinates']
            distance = haversine_distance(start_coordinates, end_coordinates)
            return Response(dumps({"distance": distance}), mimetype='application/json', status=200)
        except Exception as e:
            return Response(dumps({"error": f"An error has occurred: {str(e)}"}), mimetype='application/json', status=400)
