from .base import BaseTest
from .. import csv_handler, sqlite3_handler


class Test(BaseTest):

    csv_test_table = 'to_test_csv_import'

    def setUp(self):

        # Connect to db
        success, connection = sqlite3_handler.connect()

        # Drop table if exists
        sqlite3_handler.execute(
            connection,
            'DROP TABLE IF EXISTS %s;' % (self.csv_test_table)
        )

        # Creating a test table
        sqlite3_handler.execute(
            connection,
            'CREATE TABLE %s (a text, b text, c text);' % (self.csv_test_table)
        )

    def test_rows_to_csv(self):
        # Simulate query output
        rows = [(1, 2, 3), ('some', 'value', 'he"re')]

        assert csv_handler.rows_to_csv(rows) == '1,2,3\nsome,value,"he""re"\n'

    def test_rows_to_csv_delimiter(self):
        # Simulate query output
        rows = [(1, 2, 3), ('some', 'value', 'he"re')]

        assert csv_handler.rows_to_csv(
            rows, delimiter=';') == '1;2;3\nsome;value;"he""re"\n'

    def test_rows_to_csv_quotechar(self):
        # Simulate query output
        rows = [(1, 2, 3), ('some', 'value', 'he~re')]

        assert csv_handler.rows_to_csv(
            rows, quotechar='~') == '1,2,3\nsome,value,~he~~re~\n'

    def test_import_from_csv(self):
        # Simulate input
        body = "a,c,c\nd,e,f"

        success, message = csv_handler.import_from_csv(
            self.csv_test_table, body)

        assert success is True
        assert message is None

    def test_import_from_csv_invalid_connection(self):
        # Test import from CSV with a failed connection

        # Simulate input
        body = "a,b,c\nd,e,f"

        # Save db path
        old_path = sqlite3_handler.db_path

        # Set invalid path
        sqlite3_handler.db_path = None

        # Attempt import (will fail)
        success, message = csv_handler.import_from_csv(
            self.csv_test_table, body)

        assert success is False
        assert isinstance(message, str)

        # Restore path
        sqlite3_handler.db_path = old_path

    def test_import_from_csv_invalid_table(self):
        # Test import from CSV with an invalid table name

        # Simulate input
        table = 'invalid'
        body = "a,c,c\nd,e,f"

        success, message = csv_handler.import_from_csv(table, body)

        assert success is False
        assert message == 'no such table: invalid'

    def test_import_from_csv_invalid_body(self):
        # Test import from CSV with a malformed

        # Simulate input
        body = "a,b,c,d,e,f\ng,h,i,j,k,l"  # More columns in CSV than in table

        success, message = csv_handler.import_from_csv(
            self.csv_test_table, body)

        assert success is False
        assert isinstance(message, str)

    def test_parse_csv(self):
        # Parse a simple CSV

        assert csv_handler.parse_csv("a,c,c\nd,e,f") == [
            ['a', 'c', 'c'], ['d', 'e', 'f']]

    def test_parse_csv_delimiter(self):
        # Parse a simple CSV with a custom delimiter

        assert csv_handler.parse_csv("a;c;c\nd;e;f", delimiter=';') == [
            ['a', 'c', 'c'], ['d', 'e', 'f']]

    def test_parse_csv_quotechar(self):
        # Parse a simple CSV with a custom quotechar

        assert csv_handler.parse_csv("a,~c~,c\nd,~e~,~fg~~hi~", quotechar='~') == [
            ['a', 'c', 'c'], ['d', 'e', 'fg~hi']]
