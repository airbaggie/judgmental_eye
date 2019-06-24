Judgmental Eye: A Movie Rating App
===================================

### The Project
The Judgmental Eye is a movie ratings application where users can log in and rate movies they have seen.<br />
It uses Pearson Correlation to predict how a user will rate a movie they have not yet seen.<br />
Static data comes from MovieLens dataset, which contains 100,000 ratings of 1,700 movies from 1,000 users.<br />

### Technologies
Backend: Python, Flask, PostgreSQL, SQLAlchemy<br />
Frontend: JavaScript, HTML, Bootstrap<br />

### Environment
```
$ pip install -r requirements.txt
$ createdb ratings
$ python model.py
$ python seed.py
$ python server.py
```
