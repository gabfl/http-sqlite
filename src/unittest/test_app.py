import json

from .base import BaseTest
from .. import sqlite3_handler


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
        """ Test query with no token """

        rv = self.client.post(
            '/',
            data='SELECT 1'
        )

        # Payload is unsuccessful
        assert rv.status_code == 412

        # Validate error message
        assert b'Missing X-Auth-Token header' in rv.data

    def test_query_invalid_token(self):
        """ Test query with invalid token """

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

    def test_to_csv(self):
        """ Test query to /to_csv """

        rv = self.client.get(
            '/to_csv',
            data='SELECT 123, 456',
            headers={'X-Auth-Token': self.app.config['TOKEN']}
        )

        # Payload is successful
        assert rv.status_code == 200
        assert rv.data == b'123,456\n'

    def test_to_csv_invalid_query(self):
        """ Test query to /to_csv (invalid query) """

        rv = self.client.get(
            '/to_csv',
            data='SELECT * FROM invalid',
            headers={'X-Auth-Token': self.app.config['TOKEN']}
        )

        # Payload is unsuccessful
        assert rv.status_code == 400
        assert b'no such table' in rv.data

    def test_to_csv_empty_dataset(self):
        """ Test query to /to_csv (empty result) """

        rv = self.client.get(
            '/to_csv',
            data='SELECT 1 WHERE 1 = 2',
            headers={'X-Auth-Token': self.app.config['TOKEN']}
        )

        # Payload is successful but the result is empty
        assert rv.status_code == 200
        assert rv.data == b'Empty\n'

    def test_to_csv_missing_body(self):
        """ Test query to /to_csv (missing query) """

        rv = self.client.get(
            '/to_csv',
            headers={'X-Auth-Token': self.app.config['TOKEN']}
        )

        # Payload is unsuccessful
        assert rv.status_code == 400
        assert rv.data == b'Missing body\n'

    def test_from_csv(self):
        # Simulate input
        table = 'to_test_csv_import'

        success, connection = sqlite3_handler.connect()

        # Drop table if exists
        sqlite3_handler.execute(
            connection,
            'DROP TABLE IF EXISTS %s;' % (table)
        )

        # Creating a test table
        sqlite3_handler.execute(
            connection,
            'CREATE TABLE %s (a text, b text, c text);' % (table)
        )

        rv = self.client.post(
            '/from_csv',
            data="a,c,c\nd,e,f",
            headers={
                'X-Auth-Token': self.app.config['TOKEN'],
                'X-Table': table
            }
        )

        # Payload is successful
        assert rv.status_code == 200

        # Validate response
        body = rv.json
        assert body['success'] is True
        assert body['message'] is None

    def test_from_csv_missing_body(self):
        """ Test query to /from_csv (missing CSV in body) """

        rv = self.client.post(
            '/from_csv',
            headers={
                'X-Auth-Token': self.app.config['TOKEN'],
                'X-Table': 'some_table'
            }
        )

        # Payload is unsuccessful
        assert rv.status_code == 400

        # Validate error message
        body = rv.json
        assert body['success'] is False
        assert body['message'] == 'Missing CSV in body'

    def test_from_csv_missing_table(self):
        """ Test query to /from_csv (missing table) """

        rv = self.client.post(
            '/from_csv',
            data='a,b,c\nd,e,f',
            headers={'X-Auth-Token': self.app.config['TOKEN']}
        )

        # Payload is unsuccessful
        assert rv.status_code == 400

        # Validate error message
        body = rv.json
        assert body['success'] is False
        assert body['message'] == 'Missing table in X-Table'
