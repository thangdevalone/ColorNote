from source import db
from source.main.model.users import Users
from flask import jsonify, request,make_response
from passlib.hash import pbkdf2_sha256
from source import app
from flask_jwt_extended import create_access_token
def loginUser():
    if (request.method == 'POST'):
        json = request.json
        try:
            User = Users.query.filter(Users.user_name == json["user_name"]).first()
            if (User):
                print(User)
                if(pbkdf2_sha256.verify(json["password"],User.password_hash)):
                    return {'status': 200, 'message': 'Login successfully','user':{'id':User.id,'name':User.name,'gmail':User.gmail},'jwt':create_access_token(identity=app.config['SECRET_KEY'])},200
            return make_response(jsonify({'status': 400, 'message': 'Password or user name has some wrong'}),400)
        except:
            return make_response(jsonify({'status': 400, 'message': 'Password or user name has some wrong'}),400)