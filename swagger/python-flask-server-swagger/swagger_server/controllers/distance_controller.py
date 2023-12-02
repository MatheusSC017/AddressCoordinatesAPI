import connexion
import six

from swagger_server.models.address import Address  # noqa: E501
from swagger_server import util


def distance_addresses_get(start_address, end_address):  # noqa: E501
    """Return the distance between two given addresses

     # noqa: E501

    :param start_address: 
    :type start_address: dict | bytes
    :param end_address: 
    :type end_address: dict | bytes

    :rtype: float
    """
    if connexion.request.is_json:
        start_address = Address.from_dict(connexion.request.get_json())  # noqa: E501
    if connexion.request.is_json:
        end_address = Address.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def distance_closest_get(lat, lng):  # noqa: E501
    """Return an object with the closest location to the given coordinates and the distance in meters

     # noqa: E501

    :param lat: 
    :type lat: float
    :param lng: 
    :type lng: float

    :rtype: object
    """
    return 'do some magic!'


def distance_registers_get(start_id_address, end_id_address):  # noqa: E501
    """Return the distance between two given registers

     # noqa: E501

    :param start_id_address: 
    :type start_id_address: str
    :param end_id_address: 
    :type end_id_address: str

    :rtype: float
    """
    return 'do some magic!'
