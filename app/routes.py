from flask_restx import Resource, Namespace
from flask_jwt_extended import (create_access_token, 
                                create_refresh_token, jwt_required, 
                                get_jwt_identity)
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

            user = Users.query.filter((Users.username == data.get('username')) | (Users.email == data.get('email'))).first()
            password = data.get('password')

            if subject:
                access_token = create_access_token(identity=data.get('email'))
                refresh_token = create_refresh_token(identity=data.get('email'))

                response = make_response(jsonify(
                    {
                        "username": data.get('name'),
                        "access_token": access_token, 
                        "refresh_token": refresh_token, 
                        "id": user.id,  
                    },
                    201
                ))
                response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True)

                return response
               
            elif (user) and (user.authenticate(password) == True):
                    access_token = create_access_token(identity=user.email)
                    refresh_token = create_refresh_token(identity=user.email)

                    response = make_response(jsonify(
                        {
                            "username": user.username,
                            "access_token": access_token,
                            "refresh_token": refresh_token,  
                            "id": user.id,  
                        },
                        201
                    ))
                    return response
            
            return jsonify ({"error": "Invalid Username or Password"}), 400

        except ValueError:
            raise BadRequest(["validation errors"])  
        
@ns.route('/refresh')
class RefreshSession(Resource):
    @jwt_required(refresh=True)
    def get(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)

        return make_response(
            jsonify({"new_access_token": new_access_token}),
            200
        )

@ns.route('/watchlist')
class AddToWatchlist(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        
        current_user = get_jwt_identity()

        user = Users.query.filter_by(email=current_user).first()

        existing_in_watchlist = db.session.query(Watchlist).filter(Watchlist.movie_id == data.get('id'), 
                                                                   Watchlist.user_id == user.id).first()
        
        if existing_in_watchlist:
            return jsonify({'Msg': "Already in watchlist"}), 401
        
        else:
            if user:
                new_movie = Watchlist(
                    poster = data.get('poster_path'),
                    title = data.get('name'),
                    movie_id = data.get('id'),
                    overview = data.get('overview'),
                    user_id = user.id
                )
                db.session.add(new_movie)
                db.session.commit()

                response = make_response(
                    jsonify(
                        {
                            "poster": new_movie.poster,
                            "title": new_movie.title,  
                            "overview": new_movie.overview,
                            "id": new_movie.id    
                        },
                        201
                    )
                )

                return response
            
@ns.route('/delete/<int:movie_id>/<int:user_id>')
class DeleteFromWatchlist(Resource):
    @jwt_required()
    def delete(self, movie_id, user_id):
        in_watchlist = db.session.query(Watchlist).filter(Watchlist.movie_id == movie_id, 
                                Watchlist.user_id == user_id).first()
        
        if in_watchlist:
            db.session.delete(in_watchlist)
            db.session.commit()

            response_body = {
            "delete_successful": True,
            "message": "Review deleted."    
            }

            response = make_response(
                jsonify(response_body),
                200
            )

            return response


            
  





       






        
            
