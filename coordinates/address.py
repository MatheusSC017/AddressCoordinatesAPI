import functools
from flask import (
    Blueprint, flash, render_template, request
)
from coordinates.db import get_address_collection

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

        if error is None:
            address_collection = get_address_collection()
            try:
                address_collection.insert_one(address)
            except Exception as e:
                error = f'There was an error entering the requested address: {e}'

        if error is not None:
            flash(error)

    return render_template('address/register.html')
