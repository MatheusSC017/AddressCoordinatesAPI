from flask import request


def check_required_fields(address, required_fields):
    errors = []

    for field in required_fields:
        if field not in address or address[field] == '':
            errors.append(f'{field} is required.'.capitalize())

    return errors
