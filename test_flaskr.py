import os
import unittest
import json
import requests
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth

from flaskr.app import create_app
from models.models import *


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
            "age": 29,
            "name": "Taylor Lautner"
        }
        self.update_movie = {
            "title": "Black Swan",
            "release_date": "05-02-2018"
        }
        self.update_actor = {
            "name": "Taylor Lautner",
            "gender": "Male",
            "age": 32
        }
        self.assistant = {
            "username": "castingassistant@chitown.com",
            "password": "castingassistant#1"
        }
        self.director = {
            "username": "castingdirector@chitown.com",
            "password": "castingdirector#1"
        }
        self.producer = {
            "username": "execproducer@chitown.com",
            "password": "execproducer#1"
        }
    
    def tearDown(self):
        """Executed after each test"""
        pass

    def test_create_actor(self):
        headers = self.get_user_token(self.director['username'], self.director['password'], "create:actor")
        #res = requests.post('/actors', headers=headers, json=self.create_actor)
        print(self.client())
        res = self.client().post('/actors', headers=headers, json=self.create_actor)
        print(res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.data['success'])

    def test_get_actors(self):
        headers = self.get_user_token(self.assistant['username'], self.assistant['password'], "read:actors")
        res = self.client().get('/actors', headers=headers)
        print(res.data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    # def test_delete_question(self):
    #     res = self.client().delete('/questions/2')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_404_on_delete(self):
    #     res = self.client().delete('/questions/-1')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)

    # def test_400_for_create_without_body(self):
    #     res = self.client().post('/questions')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 400)

    # def test_successful_create_question(self):
    #     res = self.client().post('/questions', json=self.good_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    
    # def test_400_on_create_with_invalid_body(self):
    #     res = self.client().post('/questions', json=self.bad_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 400)
    
    # def test_404_if_create_question_not_allowed(self):
    #     res = self.client().post('/questions/hello')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)

    # def test_search_for_question(self):
    #     res = self.client().post('/questions/search', json=self.search_term)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(len(data['questions']))
    #     self.assertTrue(data['total_questions'])
    #     self.assertEqual(data['current_category'], None)

    # def test_400_if_search_is_empty(self):
    #     res = self.client().post('/questions/search', json=self.empty_search)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 400)

    # def test_404_if_search_not_allowed(self):
    #     res = self.client().post('/questions/search/hello')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)

    # def test_get_paginated_questions_by_category(self):
    #     res = self.client().get('/categories/2/questions')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(len(data['questions']))
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(data['current_category'])

    # def test_404_if_no_questions_found_for_category(self):
    #     res = self.client().get('/categories/2000/questions')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)

    # def test_404_if_category_filtering_not_allowed(self):
    #     res = self.client().get('/categories/questions')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)

    # def test_get_quiz_question_for_category(self):
    #     res = self.client().post('/quizzes', json=self.good_quiz_arguments)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     assert data['question'] is not None

    # def test_404_if_no_questions_found(self):
    #     res = self.client().post('/quizzes', json=self.bad_quiz_arguments)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)

    # def test_404_if_get_next_quiz_question_not_allowed(self):
    #     res = self.client().post('/quizzes/1', json=self.good_quiz_arguments)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)

    def get_auth_token():
        conn = http.client.HTTPSConnection("udacity-coffee-full-stack.us.auth0.com")
        payload = "{\"client_id\":\"oRlKYzKqkbuY3OSNIxT1zk44vpvusYVi\",\"client_secret\":\"BYJtppr1vlF4BnPvd_SFHjc09ueeDtLczH2iO-F6Tx88ZwfqoiY-yTi78c1WLbuG\",\"audience\":\"https://localhost:5000\",\"grant_type\":\"client_credentials\"}"
        headers = { 'content-type': "application/json" }
        conn.request("POST", "/oauth/token", payload, headers)

        res = conn.getresponse()
        
        return res.read().decode("utf-8")
    
    def get_user_token(self, userName, password, scope):
    # client id and secret come from LogIn (Test Client)! which has password enabled under "Client > Advanced > Grant Types > Tick Password"
        url = 'https://udacity-coffee-full-stack.us.auth0.com/oauth/token' 
        headers = {'content-type': 'application/json'}
        parameter = { "client_id": 'oRlKYzKqkbuY3OSNIxT1zk44vpvusYVi',
                    "client_secret": 'BYJtppr1vlF4BnPvd_SFHjc09ueeDtLczH2iO-F6Tx88ZwfqoiY-yTi78c1WLbuG',
                    "audience": 'https://localhost:5000',
                    "grant_type": "client_credentials",
                    "username": userName,
                    "password": password,
                    "scope": scope } 
        # do the equivalent of a CURL request from https://auth0.com/docs/quickstart/backend/python/02-using#obtaining-an-access-token-for-testing
        responseDICT = json.loads(requests.post(url, json=parameter, headers=headers).text)

        return {
            'authorization': "Bearer " + responseDICT['access_token']
        }

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()