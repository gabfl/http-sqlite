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
        assert isinstance(connection, str)

        # Restore path
        sqlite3_handler.db_path = old_path

    def test_execute(self):
        success, connection = sqlite3_handler.connect()
        rows = sqlite3_handler.execute(connection, 'SELECT 123, 456')

        assert rows == [(123, 456)]

    def test_query(self):
        # Test a valid query
        res, http_code = sqlite3_handler.run_query('SELECT 1')
        assert res['success'] is True
        assert res['result'] == [(1,)]
        assert http_code == 200

    def test_query_invalid(self):
        """
            Test a query on a non-existent table
            Throws sqlite3.OperationalError
        """

        res, http_code = sqlite3_handler.run_query('SELECT * FROM invalid')
        assert res['success'] is False
        assert isinstance(res['message'], str)
        assert http_code == 400

    def test_query_invalid_2(self):
        """
            Test execute two statements at a time
            Throws sqlite3.Warning
        """

        # Test a query on a non-existent table
        res, http_code = sqlite3_handler.run_query('SELECT 1; SELECT 2;')
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
        assert isinstance(res['message'], str)
        assert http_code == 400

        # Restore path
        sqlite3_handler.db_path = old_path

    def test_get_column_names(self):
        success, connection = sqlite3_handler.connect()

        # Drop table if exists
        rows = sqlite3_handler.execute(
            connection,
            'DROP TABLE IF EXISTS to_test_cols_names;'
        )

        # Creating a test table
        rows = sqlite3_handler.execute(
            connection,
            'CREATE TABLE to_test_cols_names (a text, b text, c text);'
        )

        # Retrieve columns
        success, columns = sqlite3_handler.get_column_names(
            'to_test_cols_names')
        assert success is True
        assert columns == ['a', 'b', 'c']

    def test_get_column_names__invalid_connection(self):
        # Retrieve columns with a failed connection

        # Save db path
        old_path = sqlite3_handler.db_path

        # Set invalid path
        sqlite3_handler.db_path = None

        # Attempt (will fail)
        success, message = sqlite3_handler.get_column_names(
            'to_test_cols_names')
        assert message
        assert success is False
        assert isinstance(message, str)

        # Restore path
        sqlite3_handler.db_path = old_path
