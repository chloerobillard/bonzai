# Importing necessary modules:
from app import create_app
import unittest
import os
import tempfile

# Initializing the app:
app = create_app()

# Setting up the unit test:
class UnitTest(unittest.TestCase):
    def setup(self):

        # Testing the app runs:
        self.db, app.config['DATABASE'] = tempfile.mkstemp()
        app.testing = True
        self.app = app.test_client()

    # Closing the app after the test has run:
    def tearDown(self):
        os.close(self.db)
        os.unlink(app.config['DATABASE'])
