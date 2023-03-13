from source import db
from source.main.model.users import Users
from flask import request
from passlib.hash import pbkdf2_sha256


def createUser():
    if (request.method == 'POST'):
        try:

            json = request.json
            if (bool(json)):
                user= Users.query.filter(Users.user_name == json["user_name"]).first()
                if(not user):
                    db.session.add(Users(
                        user_name=json['user_name'],name=json['name'], gmail=json['gmail'], password_hash=pbkdf2_sha256.hash(json["password"])))
                else:
                    return {'status': 400, 'message': 'Account already exists'}

            db.session.commit()
            return {'status': 200, 'message': 'User was created successfully'}
        except:
            return {'status': 400, 'message': 'Register fail. Please try again'}
