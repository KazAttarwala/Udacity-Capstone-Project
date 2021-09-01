import sys
import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import re

# local db path
#database_name = "casting-agency"
#database_path = "postgresql://{}/{}".format('localhost:5432', database_name)

# Heroku db path
database_path = os.getenv("DATABASE_URL")
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(Integer, nullable=False)
    release_date = Column(db.DateTime, nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except BaseException:
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except BaseException:
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except BaseException:
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date
        }


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except BaseException:
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except BaseException:
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except BaseException:
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        }
