from functools import wraps

from werkzeug.exceptions import HTTPException, default_exceptions, Aborter
from flask import Flask, request, abort

from .sqlite3_handler import run_query
from .csv_handler import rows_to_csv, import_from_csv
from .bootstrap import get_or_create_app
from .authentication import get_token

app = get_or_create_app()

# Unused, just here to force Flask to print the token to the console
get_token()


class Unauthorized(HTTPException):
    code = 401
    description = 'Invalid X-Auth-Token.'


class PreconditionFailed(HTTPException):
    code = 412
    description = 'Missing X-Auth-Token header. Token is available in src/data/token.'


default_exceptions[401] = Unauthorized
default_exceptions[412] = PreconditionFailed
abort = Aborter()


def need_authentication(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user_token = get_token()

        # Fetch authentication token
        token = request.headers.get('X-Auth-Token', '')

        # Missing or empty authentication token
        if token == '':
            abort(412)

        # Invalid user token
        if token != user_token:
            abort(401)

        return f(*args, **kwargs)

    return wrap


@app.route("/", methods=['GET', 'POST'])
@need_authentication
def query():
    # Read body
    body = request.get_data().decode('utf-8')

    if not body:
        return {
            'success': False,
            'message': 'Missing body'
        }, 400

    # Attempt to run query
    res, http_code = run_query(body)

    return {
        'success': res.get('success', 'Unknown'),
        'message': res.get('message'),
        'result': res.get('result'),
    }, http_code


@app.route("/to_csv", methods=['GET', 'POST'])
@need_authentication
def to_csv():
    # Read body
    body = request.get_data().decode('utf-8')

    if not body:
        return 'Missing body\n', 400

    # Get options
    delimiter = request.headers.get('X-Option-Delimiter', ',')
    quotechar = request.headers.get('X-Option-Quotechar', '"')

    # Attempt to run query
    res, http_code = run_query(body)

    if http_code == 200:
        csv = rows_to_csv(res.get('result', []),
                          delimiter=delimiter, quotechar=quotechar)
        return csv or 'Empty\n'
    else:
        return res.get('message', 'Unknown error') + '\n', http_code


@app.route("/from_csv", methods=['POST'])
@need_authentication
def from_csv():
    # Read body
    body = request.get_data().decode('unicode-escape').encode().decode('utf-8')

    # Get options
    table = request.headers.get('X-Table')

    if not table:
        return {
            'success': False,
            'message': 'Missing table in X-Table'
        }, 400

    if not body:
        return {
            'success': False,
            'message': 'Missing CSV in body'
        }, 400

    # Attempt to import CSV
    success, message = import_from_csv(table, body)

    return {
        'success': success,
        'message': message,
    }, 200 if success is True else 400
