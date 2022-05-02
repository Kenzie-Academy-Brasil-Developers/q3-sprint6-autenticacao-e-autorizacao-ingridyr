
from flask import jsonify, request

from app.configs.auth import auth
from app.configs.database import db

from app.models.user_model import User

from psycopg2.errors import UniqueViolation

from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError

import secrets

valid_keys = ['name', 'last_name', 'email', 'password']

def register():
    session: Session = db.session()

    data = request.get_json()
    data['api_key'] = secrets.token_urlsafe(32)

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
        return {"error": "email doesn't exists"}, 400

    if not user.verify_password(data['password']):
        print(user.verify_password(data['password']))
        return {'error': 'incorrect password'}, 400
    
    return jsonify({"api_key": user.api_key}), 200

@auth.login_required
def retrieve_user():
    user: User = auth.current_user()

    return {
        "name": user.name,
        "last_name": user.last_name,
        "email": user.email
    }, 200

@auth.login_required
def update_user():
    session: Session = db.session()
    data = request.get_json()

    user: User = User.query.filter_by(email=data["email"]).first()
    curr_user = auth.current_user()

    if not user:
        return {"error": "email doesn't exists"}, 400

    if user.id != curr_user.id:
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

@auth.login_required
def delete_user():
    session: Session = db.session()

    user = auth.current_user()
    if not user:
        return {"error": f"User doesn't exists"}, 404

    session.delete(user)
    session.commit()

    return {"msg": f'User {user.name} has been deleted'}, 200