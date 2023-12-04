from flask import Flask

from flask_migrate import Migrate
from app import models
from .extensions import api, db
from .routes import ns

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///not_netflix.db'

    api.init_app(app)
    db.init_app(app)

    migrate = Migrate(app, db)

    api.add_namespace(ns)

    return app