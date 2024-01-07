from flask import request, Response
from flask_restful import Resource
from json import dumps
from .utils import geocoding, haversine_distance
from .security import token_required
import requests
import json

fields = ['complement', 'cep', 'number', 'street', 'district', 'city', 'state', 'country', ]
required_fields = fields[3:]


def initialize_routes(api):
    api.add_resource(AddressesDistanceApi, '/v1/distance/addresses')


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

