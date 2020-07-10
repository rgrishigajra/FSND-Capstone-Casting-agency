import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr.database.models import setup_db, Movie, Actor, db
from flaskr.app import app



class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        self.app=app
        self.database_name = "casting_agency_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = self.database_path
        setup_db(self.app, self.database_path)
        db.drop_all()
        db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_case_basic(self):
        print("Default Test case:\n Testing begins:\n\n")
        self.assertTrue(True)
