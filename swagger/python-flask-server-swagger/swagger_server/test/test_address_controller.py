# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.address import Address  # noqa: E501
from swagger_server.test import BaseTestCase


class TestAddressController(BaseTestCase):
    """AddressController integration test stubs"""

    def test_api_addresses_get(self):
        """Test case for api_addresses_get

        Returns a list of addresses
        """
        response = self.client.open(
            '/api/addresses',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_addresses_post(self):
        """Test case for api_addresses_post

        Register an address
        """
        body = Address()
        response = self.client.open(
            '/api/addresses',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_addressid_delete(self):
        """Test case for api_addressid_delete

        Delete an address and return a message informing whether the deletion process was successful
        """
        response = self.client.open(
            '/api/address/<id>',
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_addressid_get(self):
        """Test case for api_addressid_get

        Return an object address
        """
        response = self.client.open(
            '/api/address/<id>',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_addressid_put(self):
        """Test case for api_addressid_put

        Update an address and return an object address with the new values
        """
        body = Address()
        response = self.client.open(
            '/api/address/<id>',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
