from flask import (
    Blueprint, flash, render_template, request, redirect, url_for
)
from .utils import geocoding
from .validations import get_fields
from .db import AddressDB

bp = Blueprint('address', __name__, url_prefix='')
address_db = AddressDB()


@bp.route('/')
def index():
    addresses = address_db.get_addresses()
    return render_template('address/index.html', addresses=addresses)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        fields = ['number', 'street', 'district', 'city', 'state', 'country', ]
        required_fields = fields

        address, error = get_fields(fields, required_fields)
        address['location'] = {'type': 'Point', 'coordinates': geocoding(address)}

        if error is not None:
            flash(error)
        else:
            address_db.register_address(address)

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
            address_db.update_address(address_id, address)

    address = address_db.get_address(address_id)
    return render_template('address/update.html', address=address)


@bp.route('/<address_id>/delete', methods=('POST', ))
def delete(address_id):
    address_db.delete_address(address_id)
    return redirect(url_for('address.index'))
