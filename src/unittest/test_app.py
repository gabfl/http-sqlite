import json

from .base import BaseTest


class Test(BaseTest):

    def test_query(self):
        """ Test query """

        rv = self.client.post(
            '/',
            data='SELECT 1234, 5678',
            headers={'X-Auth-Token': self.app.config['TOKEN']}
        )

        # Payload is successful
        assert rv.status_code == 200

        # Validate response
        body = rv.json
        assert body['success'] is True
        assert body['message'] is None
        assert body['result'] == [[1234, 5678]]

    def test_query_missing_token(self):
        """ Test query """

        rv = self.client.post(
            '/',
            data='SELECT 1'
        )

        # Payload is unsuccessful
        assert rv.status_code == 412

        # Validate error message
        assert b'Missing X-Auth-Token header' in rv.data

    def test_query_invalid_token(self):
        """ Test query """

        rv = self.client.post(
            '/',
            data='SELECT 1',
            headers={'X-Auth-Token': 'no_good'}
        )

        # Payload is unsuccessful
        assert rv.status_code == 401

        # Validate error message
        assert b'Invalid X-Auth-Token' in rv.data

    def test_query_missing_body(self):
        """ Test call to query endpoint with no query """

        rv = self.client.get(
            '/',
            headers={'X-Auth-Token': self.app.config['TOKEN']}
        )

        # Payload is unsuccessful
        assert rv.status_code == 400

        # Validate error message
        body = rv.json
        assert body['success'] is False
        assert body['message'] == 'Missing body'
