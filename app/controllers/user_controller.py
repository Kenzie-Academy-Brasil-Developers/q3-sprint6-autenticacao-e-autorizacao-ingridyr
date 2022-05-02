
from flask import jsonify, request

from datetime import timedelta

from app.configs.database import db
from app.models.user_model import User

from flask_jwt_extended import (create_access_token, get_jwt_identity, jwt_required)

from psycopg2.errors import UniqueViolation

from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.exc import IntegrityError

valid_keys = ['name', 'last_name', 'email', 'password']

def register():
    session: Session = db.session()

    data = request.get_json()

    try:
        for key in valid_keys:
                if key not in data.keys():
                    return {
                        "error": "Missing fields",
                        "expected": [key for key in valid_keys]
                    }, 400

        user: User = User(**data)

        session.add(user)

        session.commit()

    except IntegrityError as e:
        
        if type(e.orig) == UniqueViolation:
            return jsonify({"msg": "Email already exists"}), 409

    except AttributeError:
        for key, value in data.items():
            if type(value) != str:
                return {"error": "fields must be in string type"}, 400
    
    except TypeError:
        for key, value in data.items():
            if key not in valid_keys:
                return {
                        "error": "Invalid fields",
                        "accepted": [key for key in valid_keys]
                    }, 400

    return {
        "name": user.name,
        "last_name": user.last_name,
        "email": user.email
    }, 201

def login():
    data = request.get_json()

    user: User = User.query.filter_by(email=data["email"]).first()

    if not user:
        return {"error": "user doesn't exists"}, 400

    if not user.verify_password(data['password']):
        print(user.verify_password(data['password']))
        return {'error': 'incorrect password'}, 400

    token = create_access_token(user, expires_delta=timedelta(hours=4))
    
    return jsonify({'access_token': f'{token}'}), 200

@jwt_required()
def retrieve_user():
    try:
        curr_user = get_jwt_identity()

        user: User = User.query.filter_by(id=curr_user["id"]).first()
    
        return {
            "name": user.name,
            "last_name": user.last_name,
            "email": user.email
        }, 200

    except AttributeError:
        return {'error': "user doesn't exists"}, 404

@jwt_required()
def update_user():
    session: Session = db.session()
    data = request.get_json()

    user: User = User.query.filter_by(email=data["email"]).first()
    curr_user = get_jwt_identity()

    if not user:
        return {"error": "user doesn't exists"}, 400

    if user.email != curr_user['email']:
        return {"error": "invalid token"}, 401

    try:
        for key, value in data.items():
            setattr(user, key, value)

        session.add(user)

        session.commit()

    except AttributeError:
        for key, value in data.items():
            if type(value) != str:
                return {"error": "fields must be in string type"}, 400
    
    except TypeError:
        for key, value in data.items():
            if key not in valid_keys:
                return {
                        "error": "Invalid fields",
                        "accepted": [key for key in valid_keys]
                    }, 400

    return {
        "name": user.name,
        "last_name": user.last_name,
        "email": user.email
    }, 200

@jwt_required()
def delete_user():
    session: Session = db.session()

    curr_user = get_jwt_identity()
    user: User = User.query.filter_by(email=curr_user["email"]).first()

    if not curr_user:
        return {"error": f"user doesn't exists"}, 404

    try:
        session.delete(user)
        session.commit()
        
    except UnmappedInstanceError:
        return {"error": f"user doesn't exists"}, 404

    return {"msg": f'user {user.name} has been deleted'}, 200