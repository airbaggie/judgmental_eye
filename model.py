from flask_sqlalchemy import SQLAlchemy
# import correlation
from collections import defaultdict

db = SQLAlchemy()

### Model definitions ###
class User(db.Model):
    """User of this rating website"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def predict_rating(self, movie):
        """Predict user's rating of a movies"""

        return 'TODO'


class Movie(db.Model):
    """Movie on ratings website."""

    __tablename__ = 'movies'

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100))
    released_at = db.Column(db.DateTime)
    imdb_url = db.Column(db.String(200))


class Rating(db.Model):
    """Rating of a movie by a user."""

    __tablename__ = 'ratings'

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)
    score = db.Column(db.Integer)

    # Define relationship to user
    user = db.relationship('User', backref=db.backref('ratings', order_by=rating_id))

    # Define relationship to movie
    movie = db.relationship('Movie', backref=db.backref('ratings', order_by=rating_id))


##############################################################################

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use the PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == '__main__':
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app

    connect_to_db(app)
    print('Connected to DB.')