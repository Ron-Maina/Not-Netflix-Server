from flask_restx import Resource, Namespace
from flask_jwt_extended import (create_access_token, 
                                create_refresh_token, jwt_required, 
                                get_jwt_identity, set_refresh_cookies)
from flask import make_response, jsonify, request
from werkzeug.exceptions import BadRequest


from app.models import Users, Watchlist
from app.extensions import db
from .api_models import user_registration_model, user_login_model

ns = Namespace("api")

import jwt

  
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
    
@ns.route('/user/<int:id>')
class GetUserById(Resource):
    def get(self, id):
        user = Users.query.get(id)
        return jsonify(user.to_dict())
    
    
@ns.route('/register-user')
class RegisterUser(Resource):
    @ns.expect(user_registration_model)  
    def post(self):
        try:
            data = request.get_json()
            subject = data.get('sub')
            
            existing_user = Users.query.filter_by(email=data.get('email')).first()

            if existing_user:
                return jsonify({'message': 'Email already exists'}, 403)
            
            if subject:
                print(subject)
                new_user = Users(
                    username = data.get('given_name'),
                    email = data.get('email'),
                )
                db.session.add(new_user)
                db.session.commit()
            else:
                new_user = Users(
                    username = data.get('username'),
                    email = data.get('email'),
                )
                new_user.password_hash = data.get('password')

                db.session.add(new_user)
                db.session.commit()


            return jsonify(new_user.to_dict(), 201)
        
        except ValueError:
            raise BadRequest(["validation errors"])  
        
@ns.route('/login')
class Login(Resource):
    @ns.expect(user_login_model) 
    def post(self):
        try:
            data = request.get_json()
             
            subject = data.get('sub')
            user = Users.query.filter_by(username=data.get('username')).first()
            password = data.get('password')

            if subject:
                access_token = create_access_token(identity=data.get('name'))
                refresh_token = create_refresh_token(identity=data.get('name'))

                response = make_response(jsonify(
                    {
                        "username": data.get('name'),
                        "access_token": access_token,    
                    },
                    201
                ))
                response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True)

                return response
               
            elif (user) and (user.authenticate(password) == True):
                    access_token = create_access_token(identity=user.username)
                    refresh_token = create_refresh_token(identity=user.username)

                    response = make_response(jsonify(
                        {
                            "username": user.username,
                            "access_token": access_token,    
                        },
                        201
                    ))
                    response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True)
                    # set_refresh_cookies({'login': True}, refresh_token, httponly=True, secure=True)


                    return response
            
            return jsonify ({"error": "Invalid Username or Password"}), 400

        except ValueError:
            raise BadRequest(["validation errors"])  
        
@ns.route('/refresh')
class RefreshSession(Resource):
    @ns.header("Authorization", "refresh_token", required=True)
    @jwt_required(refresh=True)
    def get(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)

        return make_response(
            jsonify({"new_access_token": new_access_token}),
            200
        )

       






        
            
