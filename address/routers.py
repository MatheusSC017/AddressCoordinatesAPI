from flask import (
    Blueprint, flash, request, request, Response
)
from bson.json_util import dumps
from .utils import geocoding
from .validations import check_required_fields
from .db import AddressDB

bp = Blueprint('address', __name__, url_prefix='')
address_db = AddressDB()


@bp.route('/', methods=('GET', ))
def index():
    addresses = address_db.get_addresses()
    return Response(dumps(addresses), mimetype='application/json', status=200)


@bp.route('/register', methods=('POST', ))
def register():
    if request.method == 'POST':
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


@bp.route('/<address_id>/update', methods=('POST', ))
def update(address_id):
    if request.method == 'POST':
        fields = ['street', 'district', 'city', 'state', 'country', ]
        required_fields = fields[1:]

        address = {field: request.form.get(field, '') for field in fields}
        errors = check_required_fields(address, required_fields)

        if len(errors):
            return Response(dumps(errors), mimetype='application/json', status=200)
        else:
            address_db.update_address(address_id, address)

    address = address_db.get_address(address_id)
    return Response(dumps(address), mimetype='application/json', status=200)


@bp.route('/<address_id>/delete', methods=('POST', ))
def delete(address_id):
    address_db.delete_address(address_id)
    return Response(dumps("Registration deleted successfully"), mimetype='application/json', status=200)
