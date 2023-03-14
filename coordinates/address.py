from flask import (
    Blueprint, flash, render_template, request, abort, redirect, url_for
)
from coordinates.db import get_address_collection
from bson.objectid import ObjectId

bp = Blueprint('address', __name__, url_prefix='/address')


def get_fields(fields, required_fields):
    address = dict()
    error = None

    for field in fields:
        field_value = request.form[field]
        if field in required_fields and not field_value:
            error = f'{field} is required.'.capitalize()
            break
        address[field] = field_value

    return address, error


def get_address(address_id):
    address_collection = get_address_collection()
    address = address_collection.find_one({'_id': ObjectId(address_id)})

    if address is None:
        abort(404, 'Address not found')

    return address


@bp.route('/')
def index():
    address_collection = get_address_collection()
    addresses = address_collection.find()
    return render_template('address/index.html', addresses=addresses)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        fields = ['number', 'street', 'district', 'city', 'state', 'country', ]
        required_fields = fields

        address, error = get_fields(fields, required_fields)

        if error is not None:
            flash(error)
        else:
            address_collection = get_address_collection()
            address_collection.insert_one(address)

    return render_template('address/register.html')


@bp.route('/<address_id>/update', methods=('GET', 'POST'))
def update(address_id):
    if request.method == 'POST':
        fields = ['number', 'street', 'district', 'city', 'state', 'country', ]
        required_fields = fields

        address, error = get_fields(fields, required_fields)

        if error is not None:
            flash(error)
        else:
            address_collection = get_address_collection()
            address_collection.update_one({'_id': ObjectId(address_id)}, {'$set': address})

    address = get_address(address_id)
    return render_template('address/update.html', address=address)


@bp.route('/<address_id>/delete', methods=('POST', ))
def delete(address_id):
    address_collection = get_address_collection()
    address_collection.delete_one({'_id': ObjectId(address_id)})
    return redirect(url_for('address.index'))
