import os
from sqlalchemy import Column, String, Integer, Date, create_engine, ForeignKey, Table
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "casting_agency"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

movie_actor_table = Table('movie_actor_table', db.Model.metadata,
                          Column('movie_id', Integer, ForeignKey('movies.id')),
                          Column('actor_id', Integer, ForeignKey('actors.id')))


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Movie(db.Model):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    synopsis = Column(String)
    release_date = Column(Date)
    title = Column(String)
    genre = Column(String)

    def __init__(self, title, genre, release_date, synopsis):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def __repr__(self):
        return f"<Movie {self.id} {self.title}>"

    def format_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'genre': self.genre,
            'release_date': self.synopsis,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update():
        db.session.commit()


class Actor(db.Model):
    __tablename__ = "actors"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    gender = Column(String(6), nullable=False)
    movies = db.relationship('Movie', secondary=movie_actor_table,
                             backref='movies_list', lazy=True)

    def __repr__(self):
        return f"<Actor {self.id} {self.name}>"

    def format_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'genre': self.genre,
            'movies': self.movies,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update():
        db.session.commit()
