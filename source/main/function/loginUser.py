from source import db
from source.main.model.users import Users
from flask import request
from passlib.hash import pbkdf2_sha256


def loginUser():
    if (request.method == 'POST'):
        json = request.json
        User = Users.query.filter(Users.user_name == json["user_name"]).first()
        if (pbkdf2_sha256.verify(json["password"],User.password_hash)):
            return {'status': 200, 'message': 'Login successfully','id':User.id,'name':User.name,'gmail':User.gmail}
        else:
            return {'status': 200, 'message': 'Password or user name has some wrong'}