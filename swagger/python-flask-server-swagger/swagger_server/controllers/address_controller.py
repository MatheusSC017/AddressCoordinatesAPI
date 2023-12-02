import connexion
import six

from swagger_server.models.address import Address  # noqa: E501
from swagger_server import util


def api_addresses_get():  # noqa: E501
    """Returns a list of addresses

     # noqa: E501


    :rtype: List[object]
    """
    return 'do some magic!'


def api_addresses_post(body):  # noqa: E501
    """Register an address

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = Address.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def api_addressid_delete():  # noqa: E501
    """Delete an address and return a message informing whether the deletion process was successful

     # noqa: E501


    :rtype: str
    """
    return 'do some magic!'


def api_addressid_get():  # noqa: E501
    """Return an object address

     # noqa: E501


    :rtype: object
    """
    return 'do some magic!'


def api_addressid_put(body):  # noqa: E501
    """Update an address and return an object address with the new values

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: object
    """
    if connexion.request.is_json:
        body = Address.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
