# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.address import Address  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDistanceController(BaseTestCase):
    """DistanceController integration test stubs"""

    def test_distance_addresses_get(self):
        """Test case for distance_addresses_get

        Return the distance between two given addresses
        """
        query_string = [('start_address', Address()),
                        ('end_address', Address())]
        response = self.client.open(
            '/v1/distance/addresses',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_distance_closest_get(self):
        """Test case for distance_closest_get

        Return an object with the closest location to the given coordinates and the distance in meters
        """
        query_string = [('lat', 1.2),
                        ('lng', 1.2)]
        response = self.client.open(
            '/v1/distance/closest',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_distance_registers_get(self):
        """Test case for distance_registers_get

        Return the distance between two given registers
        """
        query_string = [('start_id_address', 'start_id_address_example'),
                        ('end_id_address', 'end_id_address_example')]
        response = self.client.open(
            '/v1/distance/registers',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
