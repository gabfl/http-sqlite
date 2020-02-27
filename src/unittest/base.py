import unittest

from .. import app, bootstrap


class BaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = bootstrap.get_or_create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['SQLITE_LOCATION'] = ':memory:'
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        pass
