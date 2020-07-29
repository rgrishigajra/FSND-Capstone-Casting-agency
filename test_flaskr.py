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
        setup_db(self.app, self.database_path)
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            # create_and_drop_all()
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_list_movies_fail_404(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        # print(data)
        if res.status_code == 404:
            self.assertFalse(data['success'])
            self.assertEqual(data['message'], 'Resource not found')

    def test_post_movies(self):
        movie = {
            "title": "Avengers",
            "release_date": "2019-01-02",
            "genre": "SuperHero"
        }
        res = self.client().post('/movies', json=movie)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        movie_db = Movie.query.get(data['movie_id'])
        movie['id'] = data['movie_id']
        self.assertEqual(movie_db.get_formatted_json(), movie)

    def test_post_movies_fail_400(self):
        movie = {
            "title": "Avengers",
            "release_date": "2019-01-02",
        }
        res = self.client().post('/movies', json=movie)
        data = json.loads(res.data)
        # print(data)
        self.assertFalse(data['success'])
        self.assertEqual(400,res.status_code)
        self.assertNotEqual(len(data['message']), 'Bad request')

    def test_list_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        # print(data)
        if res.status_code == 200:
            self.assertTrue(data['success'])
            self.assertNotEqual(len(data['movies']), 0)

    def test_delete_movie(self):
        movie=Movie.query.order_by(Movie.id).first()
        res = self.client().delete('/movie/'+str(movie.id))
        data = json.loads(res.data)
        # print(data)
        self.assertTrue(data['success'])
        movie=Movie.query.get(data['deleted'])
        self.assertEqual(movie,None)

    def test_delete_movie_fail_404(self):
        res = self.client().delete('/movie/1000')
        data = json.loads(res.data)
        # print(data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found')
        self.assertEqual(404, res.status_code)

    def test_patch_movie_fail_404(self):
        movie = {
            "title": "Avengers",
            "release_date": "2019-01-02",
        }
        res = self.client().patch('/movie/1000', json=movie)
        data = json.loads(res.data)
        print(data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found')
        self.assertEqual(404, res.status_code)

    def test_patch_movie(self):
        movie_patch = {
            "title": "Avengers 2",
            "release_date": "2019-01-02",
        }
        movie = Movie.query.order_by(Movie.id).first()
        print(movie)
        res = self.client().patch('/movie/'+str(movie.id), json=movie_patch)
        data = json.loads(res.data)
        print(data)
        self.assertTrue(data['success'])
        self.assertEqual(200, res.status_code)
        movie = Movie.query.get(data['movie']['id'])
        movie_json = movie.get_formatted_json()
        for key in movie_patch.keys():
            self.assertEqual(movie_patch[key], data['movie'][key])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
