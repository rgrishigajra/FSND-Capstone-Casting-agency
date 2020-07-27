import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr.database.models import setup_db, Movie, Actor, create_and_drop_all
from flaskr import create_app


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['DEBUG'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.database_path
        setup_db(self.app, self.database_path)
        # create_and_drop_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_case_basic(self):
        print("Default Test case:\n Testing begins:\n\n")
        self.assertTrue(True)
