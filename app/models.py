from .extensions import db
from flask_bcrypt import Bcrypt

from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property

bcrypt = Bcrypt()

class Users(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-_password_hash', '-my_watchlist.user', '-created_at')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    _password_hash = db.Column(db.String)

    my_watchlist = db.relationship("Watchlist", backref = 'user')

    @hybrid_property
    def password_hash(self):
        return 'Unauthorized'
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8')
        )
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))


class Watchlist(db.Model, SerializerMixin):
    __tablename__ = 'watchlists'

    serialize_rules = ('-user.my_watchlist', '-id')

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer)
    title = db.Column(db.String)
    poster = db.Column(db.String)
    overview = db.Column(db.String)


    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))