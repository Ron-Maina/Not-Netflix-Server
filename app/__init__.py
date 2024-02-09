import os
from flask import Flask

from flask_migrate import Migrate
from flask_cors import CORS

from app import models
from .extensions import api, db, jwt
from .routes import ns

from datetime import timedelta

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///not_netflix.db'
    app.config["JWT_SECRET_KEY"] = os.environ.get('FLASK_JWT_SECRET_KEY') 
    app.config["JWT_ALGORITHM"] = "HS256"
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)  
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=1)  



    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    
    migrate = Migrate(app, db)

    cors = CORS(app)

    api.add_namespace(ns)

    return app