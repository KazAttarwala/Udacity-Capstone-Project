import os
import unittest
import json
import requests
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth

from app import *
from models import *


class CastingTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting-agency-test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        self.oauth = OAuth(self.app)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.create_movie = {
            "title": "Black Widow",
            "release_date": "01-01-2021"
        }
        self.create_actor = {
            "gender": "Male",
            "age": 55,
            "name": "Nicholas Cage"
        }
        self.update_movie = {
            "title": "Black Swan",
            "release_date": "05-02-2018"
        }
        self.update_actor = {
            "name": "Kevin Hart",
            "gender": "Male",
            "age": 42
        }
        self.assistant = {
            "username": os.environ.get('ASSISTANT_USERNAME'),
            "password": os.environ.get('ASSISTANT_PASSWORD'),
            "jwt": {
                "authorization": os.environ.get('ASSISTANT')
            }
        }
        self.director = {
            "username": os.environ.get('DIRECTOR_USERNAME'),
            "password": os.environ.get('DIRECTOR_PASSWORD'),
            "jwt": {
                "authorization": os.environ.get('DIRECTOR')
            }
        }
        self.execproducer = {
            "username": os.environ.get('EXECPRODUCER_USERNAME'),
            "password": os.environ.get('EXECPRODUCER_PASSWORD'),
            "jwt": {
                "authorization": os.environ.get('EXECPRODUCER')
            }
        }

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_create_actor(self):
        headers = self.director['jwt']
        res = self.client().post('/actors', headers=headers, json=self.create_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_actors(self):
        headers = self.assistant['jwt']
        res = self.client().get('/actors', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_get_single_actor(self):
        headers = self.assistant['jwt']
        res = self.client().get('/actors/1', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actor'])

    def test_update_actor(self):
        headers = self.director['jwt']
        res = self.client().patch('/actors/2', headers=headers, json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor(self):
        headers = self.director['jwt']
        res = self.client().delete('/actors/3', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_movie(self):
        headers = self.execproducer['jwt']
        res = self.client().post('/movies', headers=headers, json=self.create_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_movies(self):
        headers = self.assistant['jwt']
        res = self.client().get('/movies', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_get_single_movie(self):
        headers = self.assistant['jwt']
        res = self.client().get('/movies/1', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie'])

    def test_update_movie(self):
        headers = self.director['jwt']
        res = self.client().patch('/movies/4', headers=headers, json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie(self):
        headers = self.execproducer['jwt']
        res = self.client().delete('/movies/5', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_actor_without_auth_header(self):
        res = self.client().post('/actors', json=self.create_actor)
        self.assertEqual(res.status_code, 401)

    def test_get_actors_without_auth_header(self):
        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 401)

    def test_get_single_actor_without_auth_header(self):
        res = self.client().get('/actors/2')
        self.assertEqual(res.status_code, 401)

    def test_update_actor_without_auth_header(self):
        res = self.client().patch('/actors/6', json=self.update_actor)
        self.assertEqual(res.status_code, 401)

    def test_delete_actor_without_auth_header(self):
        res = self.client().delete('/actors/6')
        self.assertEqual(res.status_code, 401)

    def test_create_movie_without_auth_header(self):
        res = self.client().post('/movies', json=self.create_movie)
        self.assertEqual(res.status_code, 401)

    def test_get_movies_without_auth_header(self):
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 401)

    def test_get_single_movie_without_auth_header(self):
        res = self.client().get('/movies/2')
        self.assertEqual(res.status_code, 401)

    def test_update_movie_without_auth_header(self):
        res = self.client().patch('/movies/6', json=self.update_movie)
        self.assertEqual(res.status_code, 401)

    def test_delete_movie_without_auth_header(self):
        res = self.client().delete('/movies/6')
        self.assertEqual(res.status_code, 401)

    def test_create_actor_for_assistant(self):
        headers = self.assistant['jwt']
        res = self.client().post('/actors', headers=headers, json=self.create_actor)

        self.assertEqual(res.status_code, 403)

    def test_update_actor_for_assistant(self):
        headers = self.assistant['jwt']
        res = self.client().patch('/actors/4', headers=headers, json=self.update_actor)

        self.assertEqual(res.status_code, 403)

    def test_delete_actor_for_assistant(self):
        headers = self.assistant['jwt']
        res = self.client().delete('/actors/4', headers=headers)

        self.assertEqual(res.status_code, 403)

    def test_create_movie_for_assistant(self):
        headers = self.assistant['jwt']
        res = self.client().post('/movies', headers=headers, json=self.create_movie)

        self.assertEqual(res.status_code, 403)

    def test_update_movie_for_assistant(self):
        headers = self.assistant['jwt']
        res = self.client().patch('/movies/4', headers=headers, json=self.update_movie)

        self.assertEqual(res.status_code, 403)

    def test_delete_movie_for_assistant(self):
        headers = self.assistant['jwt']
        res = self.client().delete('/movies/4', headers=headers)

        self.assertEqual(res.status_code, 403)

    def test_create_movie_for_director(self):
        headers = self.director['jwt']
        res = self.client().post('/movies', headers=headers, json=self.create_movie)

        self.assertEqual(res.status_code, 403)

    def test_delete_movie_for_director(self):
        headers = self.director['jwt']
        res = self.client().delete('/movies/5', headers=headers)

        self.assertEqual(res.status_code, 403)

    def test_404_on_delete_nonexisting__actor(self):
        headers = self.execproducer['jwt']
        res = self.client().delete('/actors/99', headers=headers)

        self.assertEqual(res.status_code, 404)

    def test_404_on_delete_nonexisting__movie(self):
        headers = self.execproducer['jwt']
        res = self.client().delete('/movies/99', headers=headers)

        self.assertEqual(res.status_code, 404)

    def test_400_for_create_actor_without_body(self):
        headers = self.director['jwt']
        res = self.client().post('/actors', headers=headers)

        self.assertEqual(res.status_code, 400)

    def test_400_for_create_actor_with_invalid_body(self):
        headers = self.director['jwt']
        res = self.client().post(
            '/actors',
            headers=headers,
            json={
                "gender": "Female"})

        self.assertEqual(res.status_code, 400)

    def test_400_for_create_movie_without_body(self):
        headers = self.execproducer['jwt']
        res = self.client().post('/movies', headers=headers)

        self.assertEqual(res.status_code, 400)

    def test_400_for_create_movie_with_invalid_body(self):
        headers = self.execproducer['jwt']
        res = self.client().post('/movies', headers=headers,
                                 json={"release_date": "Baaaaad"})

        self.assertEqual(res.status_code, 400)

    def test_404_for_get_nonexisting_actor(self):
        headers = self.execproducer['jwt']
        res = self.client().get('/actors/99', headers=headers)

        self.assertEqual(res.status_code, 404)

    def test_404_for_get_nonexisting_movie(self):
        headers = self.execproducer['jwt']
        res = self.client().get('/movies/99', headers=headers)

        self.assertEqual(res.status_code, 404)

    def test_404_for_update_nonexisting_movie(self):
        headers = self.execproducer['jwt']
        res = self.client().patch('/movies/99', headers=headers, json=self.update_movie)

        self.assertEqual(res.status_code, 404)

    def test_400_update_movie_without_body(self):
        headers = self.execproducer['jwt']
        res = self.client().patch('/movies/1', headers=headers)

        self.assertEqual(res.status_code, 400)

    def test_400_update_movie_with_invalid_body(self):
        headers = self.execproducer['jwt']
        res = self.client().patch('/movies/1', headers=headers,
                                  json={"release_date": "baaaaaad"})

        self.assertEqual(res.status_code, 400)

    def test_404_for_update_nonexisting_actor(self):
        headers = self.execproducer['jwt']
        res = self.client().patch('/actors/99', headers=headers, json=self.update_actor)

        self.assertEqual(res.status_code, 404)

    def test_400_update_actor_without_body(self):
        headers = self.execproducer['jwt']
        res = self.client().patch('/actors/1', headers=headers)

        self.assertEqual(res.status_code, 400)

    def test_400_update_actor_with_invalid_body(self):
        headers = self.execproducer['jwt']
        res = self.client().patch(
            '/actors/1',
            headers=headers,
            json={
                "age": "baaaaaad"})

        self.assertEqual(res.status_code, 400)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
