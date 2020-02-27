from io import StringIO
import csv
import tempfile
import sqlite3

from . import sqlite3_handler


def rows_to_csv(rows, delimiter=',', quotechar='"'):
    """ Transform SQLite rows to CSV """

    # Open a temporary file
    with tempfile.NamedTemporaryFile('w+') as file_:
        # Write all rows to a temporary file
        wr = csv.writer(file_, delimiter=delimiter,
                        quotechar=quotechar, quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            wr.writerow(list(row))

        # Flush to actually write rows even if there is a pending buffer
        file_.flush()

        # Read finalized CSV
        with open(file_.name, 'r') as f:
            lines = f.read()

    return lines


def import_from_csv(table, body, delimiter=',', quotechar='"'):
    # Connect to the database
    success, connection = sqlite3_handler.connect()

    # Return error if the connection failed
    if success is False:
        return False, connection

    # Get column names
    columns = sqlite3_handler.get_column_names(connection, table)

    # If there is no result, table does not exists
    if columns == []:
        return False, 'no such table: %s' % table

    # Prepare columns
    columns_str = ', '.join(columns)  # ['a', 'b', 'c'] -> 'a, b, c'
    column_args_placeholder = (
        '?, ' * len(columns)).strip(', ')  # ['a', 'b', 'c'] -> '?, ?, ?'

    try:
        sqlite3_handler.execute(
            connection=connection,
            query='INSERT INTO %s (%s) VALUES (%s);' % (
                table, columns_str, column_args_placeholder),
            args=parse_csv(body, delimiter=delimiter, quotechar=quotechar),
            many=True
        )

        return True, None
    except sqlite3.ProgrammingError as e:  # Invalid SQL query
        return False, str(e)


def parse_csv(input, delimiter=',', quotechar='"'):
    """
        Parse a user input
        "a,c,c\nd,e,f"
        ->
        [['a', 'c', 'c'], ['d', 'e', 'f']]
    """

    # Load input to an in-memory buffer
    buff = StringIO(input)

    # Parse CSV
    reader = csv.reader(buff, delimiter=delimiter, quotechar=quotechar)
    rows = []
    for row in reader:
        rows.append(row)

    return rows
