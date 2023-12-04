from flask_restx import fields
from .extensions import api

user_input_model = api.model("UserInput", {
    "username": fields.String,
    "email": fields.String,
    "password": fields.String,
})