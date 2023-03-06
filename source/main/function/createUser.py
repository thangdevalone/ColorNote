from source import db
from source.main.model.users import Users
from flask import request

def createUser():
     if (request.method == 'POST'):
        json = request.json
        if (bool(json)):
            db.session.add(Users(name=json['name'], gmail=json['gmail']))
            
        else:
            db.session.add(Users(name=None, gmail=None))
            
        db.session.commit()
        return {'status': 200, 'message': 'Note was created successfully'}