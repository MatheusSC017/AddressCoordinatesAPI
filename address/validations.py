from flask import request


def validate_required_fields(address, required_fields):
    for field in required_fields:
        if field not in address or address[field] == '':
            raise ValueError(f'{field} is required.'.capitalize())

