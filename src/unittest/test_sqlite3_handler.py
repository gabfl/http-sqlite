import json
import sqlite3

from .base import BaseTest
from .. import sqlite3_handler


class Test(BaseTest):

    def test_connect(self):

        success, connection = sqlite3_handler.connect()
        assert success is True
        assert isinstance(connection, sqlite3.Connection)

    def test_connect_fail(self):
        # Save db path
        old_path = sqlite3_handler.db_path

        # Set invalid path
        sqlite3_handler.db_path = None

        # Attempt connection (will fail)
        success, connection = sqlite3_handler.connect()
        assert success is False
        assert connection == 'expected str, bytes or os.PathLike object, not NoneType'

        # Restore path
        sqlite3_handler.db_path = old_path

    def test_query(self):
        # Test a valid query
        res, http_code = sqlite3_handler.run_query('SELECT 1')
        assert res['success'] is True
        assert res['result'] == [(1,)]
        assert http_code == 200

    def test_query_invalid(self):
        # Test a query on a non-existent table
        res, http_code = sqlite3_handler.run_query('SELECT * FROM invalid')
        assert res['success'] is False
        assert isinstance(res['message'], str)
        assert http_code == 400

    def test_query_invalid_connection(self):
        # Test a query with a failed connection

        # Save db path
        old_path = sqlite3_handler.db_path

        # Set invalid path
        sqlite3_handler.db_path = None

        # Attempt connection (will fail)
        res, http_code = sqlite3_handler.run_query('SELECT 1')
        assert res['success'] is False
        assert res['message'] == 'expected str, bytes or os.PathLike object, not NoneType'
        assert http_code == 400

        # Restore path
        sqlite3_handler.db_path = old_path
