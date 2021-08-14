import os
import sys
from flask import Flask, request, abort, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import json
from models import *
from auth import *
from datetime import datetime

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, static_folder='frontend/build', static_url_path='')
  setup_db(app)
  CORS(app)

  return app

APP = create_app()
migrate = Migrate(APP, db)

@APP.route('/')
def serve():
  return send_from_directory(APP.static_folder, 'index.html')

#Actor Routes
@APP.route('/actors')
@requires_auth('read:actors')
def get_actors(payload):
  try:
    actors = list(map(Actor.format, Actor.query.order_by(Actor.id).all()))

    return jsonify({
      "actors": actors
    })
  except:
    print(sys.exc_info())
    abort(500, "Something went wrong! Please try again.")


@APP.route('/actors/<int:actor_id>')
@requires_auth('read:actors')
def get_single_actor(payload, actor_id):
  try:
    actor = Actor.query.get(actor_id).format()

    if (actor is None):
      abort(404, "That actor does not exist in the database.")

    return jsonify({
      "actor": actor
    })
  except:
    print(sys.exc_info())
    abort(500, "Something went wrong! Please try again.")

@APP.route('/actors', methods=["POST"])
@requires_auth('create:actor')
def create_actor(payload):
  try:
    body = request.get_json()
    name = body.get('name').strip()
    age = body.get('age')
    gender = body.get('gender').strip()
    
    actor = Actor(name, age, gender)
    actor.insert()

    return jsonify({
      "success": True
    },200)
  except:
    print(sys.exc_info())
    abort(400, "Could not add the actor to the database. Make sure you have filled out all of the fields.")

@APP.route('/actors/<int:actor_id>', methods=["DELETE"])
@requires_auth('delete:actor')
def delete_actor(payload, actor_id):
  try:
    actor = Actor.query.get(actor_id)
    
    if (actor is None):
      abort(404, "The actor you are trying to delete does not exist in the database.")
    
    actor.delete()

    return jsonify({
      "success": True
    },200)
  except:
      print(sys.exc_info())
      abort(500, "Something went wrong! Please try again.")

@APP.route('/actors/<int:actor_id>', methods=["PATCH"])
@requires_auth('update:actor')
def update_actor(payload, actor_id):
  try:
    requested_actor = Actor.query.get(actor_id)
    
    body = request.get_json()
    name = body.get('name').strip()
    age = body.get('age')
    gender = body.get('gender').strip()

    if (requested_actor is None):
        abort(404, "The actor you are trying to update does not exist in the database.")
    
    requested_actor.name = name
    requested_actor.age = age
    requested_actor.gender = gender
    requested_actor.update()

    return jsonify({
        "success": True
    }, 200)
    
  except:
    print(sys.exc_info())
    abort(400, "Could not add the actor to the database. Make sure you have filled out all of the fields.")
    

#Movie Routes
@APP.route('/movies')
@requires_auth('read:movies')
def get_movies(payload):
  try:
    movies = list(map(Movie.format, Movie.query.order_by(Movie.id).all()))

    for movie in movies:
      movie['release_date'] = movie['release_date'].strftime("%m/%d/%Y")

    return jsonify({
      "movies": movies
    })
  except:
    print(sys.exc_info())
    abort(500, "Something went wrong! Please try again.")

@APP.route('/movies/<int:movie_id>')
@requires_auth('read:movies')
def get_single_movie(payload, movie_id):
  try:
    movie = Movie.query.get(movie_id).format()

    if (movie is None):
      abort(404, "That movie does not exist in the database.")

    return jsonify({
      "movie": movie
    })
  except:
    print(sys.exc_info())
    abort(500, "Something went wrong! Please try again.")

@APP.route('/movies', methods=['POST'])
@requires_auth('create:movie')
def create_movie(payload):
  try:
    body = request.get_json()
    title = body.get('title').strip()
    release_date = body.get('release_date')
    
    movie = Movie(title, release_date)
    movie.insert()

    return jsonify({
      "success": True
    },200)
  except:
    print(sys.exc_info())
    abort(400, "Could not add the movie to the database. Make sure you have filled out all of the fields.")

@APP.route('/movies/<int:movie_id>', methods=["DELETE"])
@requires_auth('delete:movie')
def delete_movie(payload, movie_id):
  try:
    movie = Movie.query.get(movie_id)
    
    if (movie is None):
      abort(404, "The movie you are trying to delete does not exist in the database.")
    
    movie.delete()

    return jsonify({
      "success": True
    },200)
  except:
      print(sys.exc_info())
      abort(500, "Something went wrong! Please try again.")

@APP.route('/movies/<int:movie_id>', methods=["PATCH"])
@requires_auth('update:movie')
def update_movie(payload, movie_id):
  try:
    requested_movie = Movie.query.get(movie_id)
    
    body = request.get_json()
    title = body.get('title').strip()
    release_date = body.get('release_date')

    if (requested_movie is None):
        abort(404, "The movie you are trying to update does not exist in the database.")
    
    requested_movie.title = title
    requested_movie.release_date = release_date
    requested_movie.update()

    return jsonify({
        "success": True
    }, 200)
    
  except:
    print(sys.exc_info())
    abort(400, "Could not add the movie to the database. Make sure you have filled out all of the fields.")


#Error Handlers
@APP.errorhandler(422)
def unprocessable(error):
  return jsonify({
      "success": False,
      "error": 422,
      "message": error.description
  }), 422

@APP.errorhandler(404)
def not_found(error):
  return jsonify({
      "success": False,
      "error": 404,
      "message": error.description
  }, 404)

@APP.errorhandler(400)
def bad_request(error):
  return jsonify({
    "success": False, 
    "error": 400,
    "message": error.description
  }), 400

@APP.errorhandler(500)
def server_error(error):
  return jsonify({
    "success": False, 
    "error": 500,
    "message": "Something went wrong! Please try again."
  }), 500

@APP.errorhandler(AuthError)
def handle_auth_error(ex):
  response = jsonify(ex.error)
  response.status_code = ex.status_code
  return response


if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  APP.run(host='0.0.0.0', port=port)