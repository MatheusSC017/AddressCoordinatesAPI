# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

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
        response = self.client.open(
            '/api/addresses',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
