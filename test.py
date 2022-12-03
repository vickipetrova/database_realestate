import unittest
import sys, os

from flask_testing import TestCase
from flask import Flask

from flaskr_app import db, queries
from test_data import test_data


class appDBTests(TestCase):

    def create_app(self):
        """
        Initialize flask app for testing.
        """
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['TESTING'] = True

        return self.app

    def setUp(self):
        """
        Create test data to run the tests on. 
        """
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
            # Generate the test data.
            test_data(db) 

    def tearDown(self):
        """
        Empty data before each new test. 
        """
        db.init_app(self.app)
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()