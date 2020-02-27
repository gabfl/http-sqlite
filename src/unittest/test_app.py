import json

from .base import BaseTest


class Test(BaseTest):

    def test_query(self):
        """ Test query """

        rv = self.client.post('/', data='SELECT 1234, 5678')

        # Payload is successful
        assert rv.status_code == 200

        # Validate response
        body = rv.json
        assert body['success'] is True
        assert body['message'] is None
        assert body['result'] == [[1234, 5678]]

    def test_query_missing_body(self):
        """ Test call to query endpoint with no query """

        rv = self.client.get('/')

        # Payload is unsuccessful
        assert rv.status_code == 400

        # Validate error message
        body = rv.json
        assert body['success'] is False
        assert body['message'] == 'Missing body'
