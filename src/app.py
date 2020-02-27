from functools import wraps

from werkzeug.exceptions import HTTPException, default_exceptions, Aborter
from flask import Flask, request, abort

from .sqlite3_handler import run_query
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
    description = 'Missing X-Auth-Token header. Token is available in src/data/token'


default_exceptions[401] = Unauthorized
default_exceptions[412] = PreconditionFailed
abort = Aborter()  # don't from flask import abort


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

        # finally call f. f() now haves access to g.user
        return f(*args, **kwargs)

    return wrap


@app.route("/", methods=['GET', 'POST', 'PUT', 'DELETE'])
@need_authentication
def query():
    # Read body
    body = request.get_data().decode('utf-8')

    if not body or body == '':
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
