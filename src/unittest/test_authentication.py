import tempfile

from .base import BaseTest
from .. import authentication


class Test(BaseTest):

    def test_generate_token(self):

        token = authentication.generate_token(length=30)

        assert isinstance(token, str)
        assert len(token) == 30

    def test_create_token(self):
        # Save token path
        old_path = authentication.token_path

        # Set temporary path
        tmpdir = tempfile.TemporaryDirectory()
        authentication.token_path = tmpdir.name + 'token'

        # Create new token
        assert authentication.create_token() is True

        # Restore path
        authentication.token_path = old_path

    def test_get_token(self):

        # Test retrieving user token
        assert authentication.get_token() == self.app.config['TOKEN']
