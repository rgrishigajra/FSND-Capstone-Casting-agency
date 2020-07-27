from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
database_path = "postgresql://rishabhgajra@localhost:5432/casting_agency"


def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


def create_and_drop_all():
    db.drop_all()
    db.create_all()


actor_movie_relationship_table = db.Table('movies_actiors_worked_in',
                                          db.Column('movie_id', db.Integer, db.ForeignKey(
                                              'movies.id'), primary_key=True),
                                          db.Column('actor_id', db.Integer, db.ForeignKey(
                                              'actors.id'), primary_key=True)
                                          )


class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    gender = db.Column(db.String(), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_formatted_json(self):
        return({
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        })

    def __repr__(self):
        return f'Actor: {self.id}, {self.name}'


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    release_date = db.Column(db.Date(), nullable=False)
    genre = db.Column(db.String(), nullable=False, default='')
    actors = db.relationship('Actor', secondary=actor_movie_relationship_table,
                             backref=db.backref('movie', lazy=True))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_formatted_json(self):
        return({
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "genre": self.genre
        })

    def __repr__(self):
        return f'Movie:{self.id}, {self.title}'
