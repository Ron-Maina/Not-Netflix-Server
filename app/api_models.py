from flask_restx import fields
from .extensions import api

user_registration_model = api.model("Signup", {
    "username": fields.String,
    "email": fields.String,
    "password": fields.String,
})

user_login_model = api.model("Login", {
    "username": fields.String,
    "password": fields.String,
})

