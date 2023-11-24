from flask import request


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
