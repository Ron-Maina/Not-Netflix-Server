from flask_restx import Resource, Namespace
from flask import make_response, jsonify, request
from werkzeug.exceptions import BadRequest


from app.models import Users, Watchlist
from app.extensions import db
from .api_models import user_input_model

ns = Namespace("api")

  
@ns.route('/users')
class GetUsers(Resource):
    def get(self):
        user_list = []
        for user in Users.query.all():
            user_list.append(user.to_dict())

        result = make_response(
            jsonify(user_list),
            200
        )
        return result

    @ns.expect(user_input_model)  
    def post(self):
        try:
            data = request.get_json()

            existing_user = Users.query.filter_by(email=data.get('email')).first()

            if existing_user:
                return jsonify({'message': 'Email already exists'}, 403)
            
            new_user = Users(
                username = ns.payload['username'],
                email = ns.payload['email'],
            )
            new_user.password_hash = ns.payload['password']

            db.session.add(new_user)
            db.session.commit()


            return jsonify(new_user.to_dict(), 201)
        
        except ValueError:
            raise BadRequest(["validation errors"])  
        

@ns.route('/user/<int:id>')
class GetUserById(Resource):
    def get(self, id):
        user = Users.query.get(id)
        return jsonify(user.to_dict())

        
            
