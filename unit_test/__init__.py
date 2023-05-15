from app import create_app
import unittest
import os
import tempfile

app = create_app()

class UnitTest(unittest.TestCase):
    def setup(self):
        self.db, app.config['DATABASE'] = tempfile.mkstemp()
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        os.close(self.db)
        os.unlink(app.config['DATABASE'])
