import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr.database.models import setup_db, Movie, Actor, create_and_drop_all
from flaskr import create_app

TEST_DATABASE_URI = os.getenv('TEST_DATABASE_URI')
ASSISTANT_TOKEN = os.getenv('ASSISTANT_TOKEN')
DIRECTOR_TOKEN = os.getenv('DIRECTOR_TOKEN')
PRODUCER_TOKEN = os.getenv('PRODUCER_TOKEN')


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, TEST_DATABASE_URI)
        self.casting_assistant = ASSISTANT_TOKEN
        self.casting_director = DIRECTOR_TOKEN
        self.executive_producer = PRODUCER_TOKEN
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            create_and_drop_all()
            # self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_post_movies(self):
        movie = {
            "title": "Avengers",
            "release_date": "2019-01-02",
            "genre": "SuperHero"
        }

        res = self.client().post('/movies',
                                 headers={
                                     "Authorization": "Bearer {}"
                                     .format(self.executive_producer)
                                 }, json=movie)
        data = json.loads(res.data)
        print(data)
        self.assertTrue(data['success'])
        movie_db = Movie.query.get(data['movie_id'])
        movie['id'] = data['movie_id']
        self.assertEqual(movie_db.get_formatted_json(), movie)
        

    def test_post_movies_fail_400(self):
        movie = {
            "title": "Avengers",
            "release_date": "2019-01-02",
        }
        res = self.client().post('/movies',
                                 headers={
                                     "Authorization": "Bearer {}"
                                     .format(self.executive_producer)
                                 }, json=movie)
        data = json.loads(res.data)
        # print(data)
        self.assertFalse(data['success'])
        self.assertEqual(400, res.status_code)
        self.assertNotEqual(len(data['message']), 'Bad request')

    def test_post_movies_fail_401(self):
        movie = {
            "title": "Avengers",
            "release_date": "2019-01-02",
        }
        res = self.client().post('/movies',
                                 headers={
                                     "Authorization": "Bearer {}"
                                     .format(self.casting_assistant)
                                 }, json=movie)
        data = json.loads(res.data)
        # print(data)
        self.assertFalse(data['success'])
        self.assertEqual(401, res.status_code)

    def test_list_movies_fail_401(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_list_movies(self):
        res = self.client().get('/movies',
                                headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.casting_assistant)
                                })
        data = json.loads(res.data)
        print(data)
        if res.status_code == 200: #since the test database maybe empty
            self.assertTrue(data['success'])
            self.assertNotEqual(len(data['movies']), 0)

    def test_delete_movie(self):
        movie = Movie.query.order_by(Movie.id).first()
        res = self.client().delete('/movies/'+str(movie.id),
                                   headers={
            "Authorization": "Bearer {}"
            .format(self.executive_producer)})
        data = json.loads(res.data)
        print(data)
        self.assertTrue(data['success'])
        movie = Movie.query.get(data['deleted'])
        self.assertEqual(movie, None)

    def test_delete_movie_fail_401(self):
        res = self.client().delete('/movies/1000')
        data = json.loads(res.data)
        # print(data)
        self.assertFalse(data['success'])
        self.assertEqual(401, res.status_code)

    def test_delete_movie_fail_404(self):
        res = self.client().delete('/movies/1000',
                                   headers={
                                       "Authorization": "Bearer {}"
                                       .format(self.executive_producer)})
        data = json.loads(res.data)
        # print(data)
        self.assertFalse(data['success'])
        self.assertEqual(404, res.status_code)

    def test_patch_movie_fail_404(self):
        movie = {
            "title": "Avengers",
            "release_date": "2019-01-02",
        }
        res = self.client().patch('/movies/1000',
                                  headers={
                                      "Authorization": "Bearer {}".format(self.casting_director)
                                  }, json=movie)
        data = json.loads(res.data)
        print(data)
        self.assertFalse(data['success'])
        self.assertEqual(404, res.status_code)

    def test_patch_movie_fail_401(self):
        movie = {
            "title": "Avengers",
            "release_date": "2019-01-02",
        }
        res = self.client().patch('/movies/1000',
                                  headers={
                                      "Authorization": "Bearer {}".format(self.casting_assistant)
                                  }, json=movie)
        data = json.loads(res.data)
        print(data)
        self.assertFalse(data['success'])
        self.assertEqual(401, res.status_code)

    def test_patch_movie(self):
        movie_patch = {
            "title": "Avengers 2",
            "release_date": "2019-01-02",
        }
        movie = Movie.query.order_by(Movie.id).first()
        print(movie)
        res = self.client().patch('/movies/'+str(movie.id),
                                  headers={
            "Authorization": "Bearer {}".format(self.casting_director)
        }, json=movie_patch)
        data = json.loads(res.data)
        print(data)
        self.assertTrue(data['success'])
        self.assertEqual(200, res.status_code)
        movie = Movie.query.get(data['movie']['id'])
        movie_json = movie.get_formatted_json()
        for key in movie_patch.keys():
            self.assertEqual(movie_patch[key], movie_json[key])

# actor tests

    def test_post_actor(self):
        actor = {
            "name": "rish",
            "gender": "male",
            "age": 22,
        }

        res = self.client().post('/actors',
                                 headers={
                                     "Authorization": "Bearer {}"
                                     .format(self.executive_producer)
                                 }, json=actor)
        data = json.loads(res.data)
        print(data)
        self.assertTrue(data['success'])
        actor_db = Actor.query.get(data['actor_id'])
        actor['id'] = data['actor_id']
        self.assertEqual(actor_db.get_formatted_json(), actor)

    def test_post_actors_fail_400(self):
        actor = {
            "name": "rish",
            "gender": "male",
        }
        res = self.client().post('/actors',
                                 headers={
                                     "Authorization": "Bearer {}"
                                     .format(self.executive_producer)
                                 }, json=actor)
        data = json.loads(res.data)
        # print(data)
        self.assertFalse(data['success'])
        self.assertEqual(400, res.status_code)
        self.assertNotEqual(len(data['message']), 'Bad request')

    def test_post_actors_fail_401(self):
        actor = {
            "name": "rish",
            "gender": "male",
            "age":  22
        }
        res = self.client().post('/actors',
                                 headers={
                                     "Authorization": "Bearer {}"
                                     .format(self.casting_assistant)
                                 }, json=actor)
        data = json.loads(res.data)
        # print(data)
        self.assertFalse(data['success'])
        self.assertEqual(401, res.status_code)

    def test_list_actors_fail_401(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_list_actors(self):
        res = self.client().get('/actors',
                                headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.casting_assistant)
                                })
        data = json.loads(res.data)
        print(data)
        if res.status_code == 200: #since the test database maybe empty
            self.assertTrue(data['success'])
            self.assertNotEqual(len(data['actors']), 0)

    def test_delete_actors(self):
        actor = Actor.query.order_by(Actor.id).first()
        res = self.client().delete('/actors/'+str(actor.id),
                                   headers={
            "Authorization": "Bearer {}"
            .format(self.executive_producer)})
        data = json.loads(res.data)
        print(data)
        self.assertTrue(data['success'])
        actor = Actor.query.get(data['deleted'])
        self.assertEqual(actor, None)

    def test_delete_actor_fail_401(self):
        res = self.client().delete('/actors/1000')
        data = json.loads(res.data)
        # print(data)
        self.assertFalse(data['success'])
        self.assertEqual(401, res.status_code)

    def test_delete_actor_fail_404(self):
        res = self.client().delete('/actors/1000',
                                   headers={
                                       "Authorization": "Bearer {}"
                                       .format(self.executive_producer)})
        data = json.loads(res.data)
        # print(data)
        self.assertFalse(data['success'])
        self.assertEqual(404, res.status_code)

    def test_patch_actor_fail_404(self):
        actor = {
            "name": "gopi",
            "gender": "male",
        }
        res = self.client().patch('/actors/1000',
                                  headers={
                                      "Authorization": "Bearer {}".format(self.casting_director)
                                  }, json=actor)
        data = json.loads(res.data)
        print(data)
        self.assertFalse(data['success'])
        self.assertEqual(404, res.status_code)

    def test_patch_actor_fail_401(self):
        actor = {
            "name": "gopi",
            "gender": "male",
        }
        res = self.client().patch('/actors/1000',
                                  headers={
                                      "Authorization": "Bearer {}".format(self.casting_assistant)
                                  }, json=actor)
        data = json.loads(res.data)
        print(data)
        self.assertFalse(data['success'])
        self.assertEqual(401, res.status_code)

    def test_patch_actor(self):
        actor = {
            "name": "gopi",
            "gender": "male",
        }
        actor_db = Actor.query.order_by(Actor.id).first()
        res = self.client().patch('/actors/'+str(actor_db.id),
                                  headers={
            "Authorization": "Bearer {}".format(self.casting_director)
        }, json=actor)
        data = json.loads(res.data)
        print(data)
        self.assertTrue(data['success'])
        self.assertEqual(200, res.status_code)
        actor_db = Actor.query.get(data['actor']['id'])
        actor_json = actor_db.get_formatted_json()
        for key in actor.keys():
            self.assertEqual(actor[key], actor_json[key])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
