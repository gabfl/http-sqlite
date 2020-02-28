import sqlite3
import os.path

from .bootstrap import get_or_create_app

app = get_or_create_app()

# Define db location
dir_path = os.path.dirname(os.path.realpath(__file__))
db_path = app.config['SQLITE_LOCATION'] if app.config.get(
    'SQLITE_LOCATION') else dir_path + '/data/sqlite.db'


def connect():
    """ Establish connection to SQLite db """

    conn = None

    try:
        conn = sqlite3.connect(db_path)
    except Exception as e:
        return (False, str(e))

    return (True, conn)


def execute(connection, query, args=[], many=False):
    """ Execute a query """

    cursor = connection.cursor()
    if many:  # Multiple execution
        cursor.executemany(query, args)
    else:  # Single execution
        cursor.execute(query, args)
    connection.commit()
    rows = cursor.fetchall()
    cursor.close()

    return rows


def run_query(query):

    # Establish db connection
    success, connection = connect()

    # Return error if the connection failed
    if success is False:
        return {
            'success': False,
            'message': connection
        }, 400

    # Execute query
    try:
        rows = execute(connection, query)
    except sqlite3.OperationalError as e:  # Invalid SQL query
        return {
            'success': False,
            'message': str(e)
        }, 400
    except sqlite3.Warning as e:  # Invalid SQL query
        return {
            'success': False,
            'message': str(e)
        }, 400

    # for row in rows:
    #     print(row)

    return {
        'success': True,
        'result': rows
    }, 200


def get_column_names(connection, table):
    """
        Returns a list of column names from a given table

        It is not possible to use a parameterized query as seen here:
        https://stackoverflow.com/questions/39985599/parameter-binding-not-working-for-sqlite-pragma-table-info

    """

    # Check for forbidden characters
    # Simple attempt to validate input since we cannot use parameterized queries
    if any(ext in table for ext in [',', '"', "'", ';']):
        return []

    rows = execute(connection, "PRAGMA TABLE_INFO ('%s')" % (table))

    return [t[1] for t in rows]
