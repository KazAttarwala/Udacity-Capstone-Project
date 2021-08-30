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
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
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
            "username": "castingassistant@chitown.com",
            "password": "castingassistant#1",
            "jwt": {
                "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlybkRPYUhWMnlMZ1c1aERKUHFWdSJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY29mZmVlLWZ1bGwtc3RhY2sudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwZjIwMjE4NjEwYTc2MDA2OWVjMDQxOCIsImF1ZCI6WyJodHRwczovL2xvY2FsaG9zdDo1MDAwIiwiaHR0cHM6Ly91ZGFjaXR5LWNvZmZlZS1mdWxsLXN0YWNrLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MzAyNjc3NDgsImV4cCI6MTYzMDM1NDE0OCwiYXpwIjoiSFl2TGgxTHg3NDl4NU9QN1RKc21xMmNRRjBKakhROVMiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIHJlYWQ6YWN0b3JzIHJlYWQ6bW92aWVzIiwicGVybWlzc2lvbnMiOlsicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.dzoXuTEG_ZaJyEQ6SjkcBWo-nmtEZh8ypTixbPWUqavEgPxPe6T9ivB4gWwJb_b3npQbLmpnmwQq12I3AUe2WjEeYe27CbalYhjpTM6IjUC4iByJVtkZlcp4Sr_EyGwpIGcfVJhOp0t6S5gTYbBBVuk2ySFi_ANAOGPrjskaFgjzMks4cIW1zrpme7Rpft7tn6KejRSdIIN-LgY0vqhtKLuxIZLBM602wBqUP_h4FKucVpj9aVZyDdJBhja_tEA20zbXTbc_DQoxlU2Fr0XMzhyNTssU0AQKzAUcYYKDajprGkLg6aTpNfH19koU6NmzgtZM3OYgDZOraDlavYPvLg"
            }
        }
        self.director = {
            "username": "castingdirector@chitown.com",
            "password": "castingdirector#1",
            "jwt": {
                "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlybkRPYUhWMnlMZ1c1aERKUHFWdSJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY29mZmVlLWZ1bGwtc3RhY2sudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwZjIwMjcxNjEwYTc2MDA2OWVjMDQzYiIsImF1ZCI6WyJodHRwczovL2xvY2FsaG9zdDo1MDAwIiwiaHR0cHM6Ly91ZGFjaXR5LWNvZmZlZS1mdWxsLXN0YWNrLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MzAyNjk4NDQsImV4cCI6MTYzMDM1NjI0NCwiYXpwIjoiSFl2TGgxTHg3NDl4NU9QN1RKc21xMmNRRjBKakhROVMiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIGNyZWF0ZTphY3RvciBkZWxldGU6YWN0b3IgdXBkYXRlOmFjdG9yIHVwZGF0ZTptb3ZpZSByZWFkOmFjdG9ycyByZWFkOm1vdmllcyIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvciIsImRlbGV0ZTphY3RvciIsInJlYWQ6YWN0b3JzIiwicmVhZDptb3ZpZXMiLCJ1cGRhdGU6YWN0b3IiLCJ1cGRhdGU6bW92aWUiXX0.K1_VCI7CsTBJGw6tg0ld6ukSobWwtMVkm1RfC3ipj7vcAx8_oRCs8cDZg9PYzJZgn7gqDKxemWV856PuQKIL9vClDgd174GC43jv5-e6NrW7PdlrlS668Jcv5Edocfmw4bwWUy5G8otcEHrJ0B_WE43jeNdRw-Rd49KMofi-5yZ0FwZsxdJQiyQ8uymGgSbPzCrSBS_-9ogBt8WtTbGMKWFUUjp-6T9pNbnn2auEAmn_0NN4TKFK1gbC3GDxSyiq65q4_eHJcITT_Zev6bmwLZvqP9I-G8027b1kJm7QtksVY4V1rBAn8QNhSQ4qfMAashn3ReQPyt6Ym0zcPPj9kA"
            }
        }
        self.execproducer = {
            "username": "execproducer@chitown.com",
            "password": "execproducer#1",
            "jwt": {
                "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlybkRPYUhWMnlMZ1c1aERKUHFWdSJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY29mZmVlLWZ1bGwtc3RhY2sudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwZjIwMmFhNjgwYjg5MDA2OGY0YjA1YSIsImF1ZCI6WyJodHRwczovL2xvY2FsaG9zdDo1MDAwIiwiaHR0cHM6Ly91ZGFjaXR5LWNvZmZlZS1mdWxsLXN0YWNrLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MzAyNzAwMTgsImV4cCI6MTYzMDM1NjQxOCwiYXpwIjoiSFl2TGgxTHg3NDl4NU9QN1RKc21xMmNRRjBKakhROVMiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIGNyZWF0ZTphY3RvciBjcmVhdGU6bW92aWUgZGVsZXRlOmFjdG9yIGRlbGV0ZTptb3ZpZSB1cGRhdGU6YWN0b3IgdXBkYXRlOm1vdmllIHJlYWQ6YWN0b3JzIHJlYWQ6bW92aWVzIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9yIiwiY3JlYXRlOm1vdmllIiwiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyIsInVwZGF0ZTphY3RvciIsInVwZGF0ZTptb3ZpZSJdfQ.iTZE7Dg1hU8R-9DaIRDoqQnO9GIcJJObzIvhkdV4Q0Glg8kWfEeBTrlEFMGbDe3UV3mFrM5nT6XOfDZ1LMNBfRxTb_ewFgPM-XXl_Gkxkynnu7wiKFdZx-M8ZeOVjr2zS3BN9ak1pBI4BI2AVbVOgKFo_3Dc9kJnoLjLwYuL6tjydvkzwfBRxxhMS8bCnjb1Ttkw9ifztBUxW8w2zyn6kLhITAaesRPaAqFZ_dyRCTJp0yEcn8pPpopg_JdtH7FjlovSpDCDWMgVDnn6JbjLy9brf_RIVjCmvop4Tefc62tE7OrNv3y3_CohaV7zLgkLGijAAkTTcIL9TVy0uiwMiQ"
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
        res = self.client().post('/actors', headers=headers, json={"gender": "Female"})

        self.assertEqual(res.status_code, 400)

    def test_400_for_create_movie_without_body(self):
        headers = self.execproducer['jwt']
        res = self.client().post('/movies', headers=headers)

        self.assertEqual(res.status_code, 400)

    def test_400_for_create_movie_with_invalid_body(self):
        headers = self.execproducer['jwt']
        res = self.client().post('/movies', headers=headers, json={"release_date": "Baaaaad"})

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
        res = self.client().patch('/movies/1', headers=headers, json={"release_date": "baaaaaad"})

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
        res = self.client().patch('/actors/1', headers=headers, json={"age": "baaaaaad"})

        self.assertEqual(res.status_code, 400)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()