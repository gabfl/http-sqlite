from .base import BaseTest
from .. import csv_handler


class Test(BaseTest):

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
