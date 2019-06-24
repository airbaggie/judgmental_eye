from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Movie, Rating

app = Flask(__name__)
app.secret_key = 'ABC'

@app.route('/')
def index():
    """Homepage."""

    return render_template('homepage.html')


@app.route('/movies')
def movie_list():
    """Show list of movies."""

    movies = Movie.query.order_by('title').all()
    return render_template('movie_list.html', movies=movies)


@app.route("/movies/<int:movie_id>", methods=['GET'])
def movie_detail(movie_id):
    """Show info about movie.
    If a user is logged in, let them add/edit a rating.
    """

    movie = Movie.query.get(movie_id)
    user_id = session.get("user_id")

    if user_id:
        user_rating = Rating.query.filter_by(
            movie_id=movie_id, user_id=user_id).first()

    else:
        user_rating = None

    # Get average rating of movie
    rating_scores = [r.score for r in movie.ratings]
    avg_rating = float(sum(rating_scores)) / len(rating_scores)

    prediction = None

    # Only predict if the user hasn't rated it
    if (not user_rating) and user_id:
        user = User.query.get(user_id)
        if user:
            prediction = user.predict_rating(movie)

    # Either use the prediction or their real rating
    if prediction:
        effective_rating = prediction
    elif user_rating:
        effective_rating = user_rating.score
    else:
        effective_rating = None

    # Get the eye's rating, either by predicting or using real rating
    the_eye = User.query.filter_by(email="the-eye@of-judgment.com").one()
    eye_rating = Rating.query.filter_by(
        user_id=the_eye.user_id, movie_id=movie.movie_id).first()

    if eye_rating is None:
        eye_rating = the_eye.predict_rating(movie)
    else:
        eye_rating = eye_rating.score

    if eye_rating and effective_rating:
        difference = abs(eye_rating - effective_rating)
    else:
        difference = None

    return render_template(
                            "movie.html",
                            movie=movie,
                            user_rating=user_rating,
                            average=avg_rating,
                            prediction=prediction,
                            eye_rating=eye_rating,
                            difference=difference
                          )


@app.route('/movies/<int:movie_id>', methods=['POST'])
def movie_detail_process(movie_id):
    """Add/edit a rating."""

    # Get form variables
    score = int(request.form['score'])

    user_id = session.get('user_id')
    if not user_id:
        raise Exception('No user logged in.')

    # Check for an existing rating
    rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()

    # Update an existing rating or if there isn't one yet, create one.
    if rating:
        rating.score = score
        flash('Rating updated.')

    else:
        rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
        flash('Rating added.')
        db.session.add(rating)

    db.session.commit()

    return redirect(f'/movies/{movie_id}')


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/users/<int:user_id>')
def user_detail(user_id):
    """Show info about user."""

    user = User.query.options(db.joinedload('ratings').joinedload('movie')).get(user_id)
    return render_template('user.html', user=user)


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template('register_form.html')


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    email = request.form['email']
    password = request.form['password']
    age = int(request.form['age'])
    zipcode = request.form['zipcode']

    new_user = User(email=email, password=password, age=age, zipcode=zipcode)

    db.session.add(new_user)
    db.session.commit()

    flash(f'User {email} added.')
    return redirect(f'/users/{new_user.user_id}')


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template('login_form.html')


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if not user:
        flash('No such user')
        return redirect('/login')

    if user.password != password:
        flash('Incorrect password')
        return redirect('/login')

    session['user_id'] = user.user_id

    flash('Logged in')
    return redirect(f'/users/{user.user_id}')


@app.route('/logout')
def logout():
    """Log out."""

    del session['user_id']
    flash('Logged Out.')
    return redirect('/')


if __name__ == '__main__':
    app.debug = True
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host='0.0.0.0')