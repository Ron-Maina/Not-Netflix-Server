from app.models import Users, Watchlist
from faker import Faker
from app.extensions import db
from app import create_app
import random

app = create_app()
fake = Faker()

with app.app_context():

    Users.query.delete()
    Watchlist.query.delete()


    user_list = []
    for i in range(1):
        user = Users(
            username = fake.name(),
            email = 'hahem61090@glalen.com',
            _password_hash = '1234',
        )
        user_list.append(user)
    db.session.add_all(user_list)
    db.session.commit()
    print('SEEDED USERS...')

    movies = []
    for i in range(3):
        movie = Watchlist(
            user_id = 1, 
            movie_id = random.randint(1,3),
            title = fake.sentence(),
            poster = fake.sentence()
            
        )
        movies.append(movie)
    db.session.add_all(movies)
    db.session.commit()
    print('SEEDED MOVIES...')

