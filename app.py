import os
import sys
from flask import Flask, request, abort, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
import json
from models import *
from auth import *
from datetime import datetime

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, static_folder='frontend/build', static_url_path='')
  setup_db(app)
  CORS(app, expose_headers='Authorization')
  migrate = Migrate(app, db)

  # @app.after_request
  # def after_request(response):
  #     response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
  #     response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,PUT,DELETE,OPTIONS')
      
  #     return response

  @app.route('/')
  def serve():
    return send_from_directory(app.static_folder, 'index.html')

  #Actor Routes
  @app.route('/actors')
  @requires_auth('read:actors')
  def get_actors(payload):
    try:
      actors = list(map(Actor.format, Actor.query.order_by(Actor.id).all()))

      return jsonify({
        "actors": actors
      })
    except:
      print(sys.exc_info())
      abort(500)


  @app.route('/actors/<int:actor_id>')
  @requires_auth('read:actors')
  def get_single_actor(payload, actor_id):
    try:
      actor = Actor.query.get(actor_id)

      if (actor is None):
        abort(404, description="That actor does not exist in the database.")

      actor = actor.format()

      return jsonify({
        "actor": actor
      })
    except:
      print(sys.exc_info())
      abort(404)

  @app.route('/actors', methods=["POST"])
  @requires_auth('create:actor')
  def create_actor(payload):
    try:
      body = request.get_json()
      name = body.get('name').strip() if len(body.get('name')) > 0 else None
      age = body.get('age')
      gender = body.get('gender').strip() if len(body.get('gender')) > 0 else None
      
      actor = Actor(name, age, gender)
      actor.insert()

      return jsonify({
        "success": True
      })
    except:
      print(sys.exc_info())
      abort(400, description="Could not add the actor to the database. Make sure you have filled out all of the fields.")

  @app.route('/actors/<int:actor_id>', methods=["DELETE"])
  @requires_auth('delete:actor')
  def delete_actor(payload, actor_id):
    try:
      actor = Actor.query.get(actor_id)
      
      if (actor is None):
        abort(404, description="The actor you are trying to delete does not exist in the database.")
      
      actor.delete()

      return jsonify({
        "success": True
      })
    except:
        print(sys.exc_info())
        abort(404)

  @app.route('/actors/<int:actor_id>', methods=["PATCH"])
  @requires_auth('update:actor')
  def update_actor(payload, actor_id):
    requested_actor = Actor.query.get(actor_id)
    if (requested_actor is None):
          abort(404, description="The actor you are trying to update does not exist in the database.")

    try:
      body = request.get_json()
      name = body.get('name').strip() if len(body.get('name')) > 0 else None
      age = body.get('age')
      gender = body.get('gender').strip() if len(body.get('gender')) > 0 else None

      requested_actor.name = name
      requested_actor.age = age
      requested_actor.gender = gender
      requested_actor.update()

      return jsonify({
          "success": True
      })
      
    except:
      print(sys.exc_info())
      abort(400, description="Could not add the actor to the database. Make sure you have filled out all of the fields.")
      

  #Movie Routes
  @app.route('/movies')
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
      abort(500)

  @app.route('/movies/<int:movie_id>')
  @requires_auth('read:movies')
  def get_single_movie(payload, movie_id):
    try:
      movie = Movie.query.get(movie_id)

      if (movie is None):
        abort(404, description="That movie does not exist in the database.")

      movie = movie.format()

      return jsonify({
        "movie": movie
      })
    except:
      print(sys.exc_info())
      abort(404)

  @app.route('/movies', methods=['POST'])
  @requires_auth('create:movie')
  def create_movie(payload):
    try:
      body = request.get_json()
      title = body.get('title').strip() if len(body.get('title')) > 0 else None
      release_date = body.get('release_date')
      
      movie = Movie(title, release_date)
      movie.insert()

      return jsonify({
        "success": True
      })
    except:
      print(sys.exc_info())
      abort(400, description="Could not add the movie to the database. Make sure you have filled out all of the fields.")

  @app.route('/movies/<int:movie_id>', methods=["DELETE"])
  @requires_auth('delete:movie')
  def delete_movie(payload, movie_id):
    try:
      movie = Movie.query.get(movie_id)
      
      if (movie is None):
        abort(404, description="The movie you are trying to delete does not exist in the database.")
      
      movie.delete()

      return jsonify({
        "success": True
      })
    except:
        print(sys.exc_info())
        abort(404)

  @app.route('/movies/<int:movie_id>', methods=["PATCH"])
  @requires_auth('update:movie')
  def update_movie(payload, movie_id):
    requested_movie = Movie.query.get(movie_id)
    if (requested_movie is None):
          abort(404, description="The movie you are trying to update does not exist in the database.")

    try:
      body = request.get_json()
      title = body.get('title').strip() if len(body.get('title')) > 0 else None
      release_date = body.get('release_date')
      
      requested_movie.title = title
      requested_movie.release_date = release_date
      requested_movie.update()

      return jsonify({
          "success": True
      })
    except:
      print(sys.exc_info())
      abort(400, description="Could not add the movie to the database. Make sure you have filled out all of the fields.")


  #Error Handlers
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": error.description
    }), 422

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": error.description
    }), 404

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": error.description
    }), 400

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "Something went wrong! Please try again."
    }), 500

  @app.errorhandler(AuthError)
  def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

  return app

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)