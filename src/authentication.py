import sqlite3
import os
import os.path
import secrets
import string
import sys

from .bootstrap import get_or_create_app

app = get_or_create_app()

# Define db location
dir_path = os.path.dirname(os.path.realpath(__file__))
token_path = dir_path + '/data/token'


def generate_token(length=48):
    """ Generate a user token """

    return ''.join(secrets.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(length))


def create_token():
    """ Create token if it does not exists """

    if not os.path.isfile(token_path):
        with open(token_path, 'w', newline='') as f:
            f.write(generate_token())

        print('new token')
        return True


def get_token():
    """ Retrieve user token """

    create_token()

    with open(token_path, 'r') as f:
        token = f.readline()

    print(' * ▾▾▾▾▾▾▾▾▾▾▾▾▾▾▾▾▾▾▾▾▾▾', file=sys.stderr)
    print(' * X-Authen-Token -> %s' % (token), file=sys.stderr)
    print(' * ▴▴▴▴▴▴▴▴▴▴▴▴▴▴▴▴▴▴▴▴▴▴', file=sys.stderr)

    # Return token set in app config or token from file
    return app.config['TOKEN'] if app.config.get('TOKEN') else token
