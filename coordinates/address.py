import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from coordinates.db import get_db

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


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        fields = ['number', 'street', 'district', 'city', 'state', 'country', ]
        required_fields = fields

        address, error = get_fields(fields, required_fields)

        if error is None:
            db = get_db()
            address_collection = db['address']
            try:
                address_collection.insert_one(address)
            except Exception as e:
                error = f'There was an error entering the requested address: {e}'

        flash(error)

    return render_template('address/register.html')
