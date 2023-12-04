from .extensions import db
from sqlalchemy_serializer import SerializerMixin


class Users(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-_password_hash', '-my_watchlist.user', '-created_at')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    _password_hash = db.Column(db.String, nullable = False)

    my_watchlist = db.relationship("Watchlist", backref = 'user')


class Watchlist(db.Model, SerializerMixin):
    __tablename__ = 'watchlists'

    serialize_rules = ('-user.my_watchlist', '-id')

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer)
    title = db.Column(db.String)
    poster = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))