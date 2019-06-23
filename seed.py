import datetime
from sqlalchemy import func
from model import User, Rating, Movie, connect_to_db, db
from server import app

def load_users():
    """Load users from u.user into database."""

    for i, row in enumerate(open('seed_data/u.user')):
        row = row.strip()
        user_id, age, gender, occupation, zipcode = row.split('|')
        user = User(user_id=user_id, age=age, zipcode=zipcode)
        db.session.add(user)
    
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    for i, row in enumerate(open('seed_data/u.item')):
        row = row.rstrip()
        movie_id, title, released_str, junk, imdb_url = row.split('|')[:5]

        if released_str:
            released_at = datetime.datetime.strptime(released_str, '%d-%b-%Y')
        else:
            released_at = None
        
        title = title[:-7]   # " (YEAR)" == 7
        
        movie = Movie(movie_id=movie_id, title=title, released_at=released_at, imdb_url=imdb_url)
        db.session.add(movie)

    db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""

    for i, row in enumerate(open('seed_data/u.data')):
        row = row.rstrip()
        user_id, movie_id, score, timestamp = row.split('\t')

        user_id = int(user_id)
        movie_id = int(movie_id)
        score = int(score)
        
        rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
        db.session.add(rating)

        if i % 1000 == 0:
            db.session.commit()

    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = 'SELECT setval('users_user_id_seq', :new_id)'
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()