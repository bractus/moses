# app/__init__.py
import json
from flask_api import FlaskAPI, status
from flask_sqlalchemy import SQLAlchemy

from flask import request, jsonify, abort, make_response

# local import

from instance.config import app_config

# For password hashing
from flask_bcrypt import Bcrypt

# initialize db
db = SQLAlchemy()


def create_app(config_name):

    from app.models import MLModel, User

    app = FlaskAPI(__name__, instance_relative_config=True)
    # overriding Werkzeugs built-in password hashing utilities using Bcrypt.
    bcrypt = Bcrypt(app)

    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/models/', methods=['POST', 'GET'])
    def models():
        # get the access token
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # Go ahead and handle the request, the user is authed
                if request.method == "POST":
                    name = str(request.data.get('name', ''))
                    mdl = request.files.get('file', None).read()
                    if name:
                        model = MLModel(name=name, model=mdl,
                                        created_by=user_id)
                        model.save()
                        response = jsonify({
                            'id': model.id,
                            'name': model.name,
                            'description': model.description,
                            'date_created': model.date_created,
                            'created_by': user_id,
                            'status_code': 201
                        })
                        return make_response(response), 201

                else:
                    # GET
                    # get all the models for this user
                    models = MLModel.get_all(user_id)
                    results = []

                    for model in models:
                        obj = {
                            'id': model.id,
                            'name': model.name,
                            'description': model.description,
                            'date_created': model.date_created,
                            'created_by': model.created_by
                        }
                        results.append(obj)

                    data = jsonify({
                        'status_code': 200,
                        'data': results
                    })

                    return make_response(data), 200
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message,
                    'status_code': 401
                }
                return make_response(jsonify(response)), 401

    @app.route('/models/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def model_manipulation(id, **kwargs):

        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                model = MLModel.query.filter_by(id=id).first()
                if not model:
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)

                if request.method == "DELETE":
                    model.delete()
                    response = {
                        "message": "model {} deleted".format(model.id),
                        "status_code": 200
                    }
                    return make_response(jsonify(response)), 200
                elif request.method == 'PUT':
                    name = str(request.data.get('name', ''))
                    model.name = name
                    model.save()
                    response = {
                        'id': model.id,
                        'name': model.name,
                        'description': model.description,
                        'date_created': model.date_created,
                        'created_by': model.created_by,
                        'status_code': 200
                    }
                    return make_response(jsonify(response)), 200
                else:
                    # GET
                    response = jsonify({
                        'id': model.id,
                        'name': model.name,
                        'description': model.description,
                        'date_created': model.date_created,
                        'created_by': model.created_by,
                        'status_code': 200
                    })
                    return make_response(response), 200
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message,
                    'status_code': 401
                }
                return make_response(jsonify(response)), 401

    # import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
