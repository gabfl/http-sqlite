from flask import Flask, request

from .sqlite3_handler import run_query
from .bootstrap import get_or_create_app

app = get_or_create_app()


@app.route("/", methods=['GET', 'POST', 'PUT', 'DELETE'])
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
