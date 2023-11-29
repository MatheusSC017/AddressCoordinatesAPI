from .app_setup import GOOGLE_MAPS_SECRET_KEY
import requests
import math


def singleton(target_class):
    instances = dict()

    def get_class(*args, **kwargs):
        if target_class not in instances:
            instances[target_class] = target_class(*args, **kwargs)
        return instances[target_class]

    return get_class


def validate_coordinates(coordinates):
    if not (-90 <= coordinates[0] <= 90) or not (-180 <= coordinates[1] <= 180):
        raise ValueError("Invalid latitude or longitude value.")


def geocoding(address):
    BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

    fields_order = ['street', 'number', 'district', 'city', 'state', 'country']
    address_string = ', '.join([str(address.get(field)) for field in fields_order if address.get(field)])

    params = {
        'address': address_string,
        'sensor': False,
        'region': 'br',
        'key': GOOGLE_MAPS_SECRET_KEY
    }

    response = requests.get(BASE_URL, params=params)
    result = response.json()
    if not result['results']:
        raise ValueError("Invalid Address, no coordinates were found for the address provided")

    lat = result['results'][0]['geometry']['location']['lat']
    lng = result['results'][0]['geometry']['location']['lng']

    return [lat, lng]


def haversine_distance(start_coordinate, end_coordinate):
    EARTH_RADIUS = 3958.8
    radius_start_lat = start_coordinate[0] * (math.pi/180)
    radius_end_lat = end_coordinate[0] * (math.pi/180)
    difference_lat = radius_start_lat - radius_end_lat
    difference_lng = (start_coordinate[1] - end_coordinate[1]) * (math.pi/180)

    distance = 2 * EARTH_RADIUS * math.asin(math.sqrt(
        math.pow(math.sin(difference_lat / 2), 2) +
        math.cos(radius_start_lat) *
        math.cos(radius_end_lat) *
        math.pow(math.sin(difference_lng / 2), 2))
    )

    return distance * 1609.344
