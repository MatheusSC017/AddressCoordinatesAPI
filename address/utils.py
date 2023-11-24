from .app_setup import GOOGLE_MAPS_SECRET_KEY
import requests


def geocoding(address):
    BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

    fields_order = ['street', 'number', 'district', 'city', 'state', 'country']
    address_string = ', '.join([str(address[field]) for field in fields_order])

    params = {
        'address': address_string,
        'sensor': False,
        'region': 'br',
        'key': GOOGLE_MAPS_SECRET_KEY
    }

    response = requests.get(BASE_URL, params=params)
    result = response.json()

    print(result['results'][0]['geometry'])
    lat = result['results'][0]['geometry']['location']['lat']
    lng = result['results'][0]['geometry']['location']['lng']

    return [lat, lng]