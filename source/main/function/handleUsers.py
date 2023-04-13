from source import db
from source.main.model.users import Users
from flask import request,make_response,jsonify

from passlib.hash import pbkdf2_sha256
def handleUsers(param):
    
    if (request.method == 'DELETE'):
        try:
            json = request.json
            user = Users.query.get(param)
            if(pbkdf2_sha256.verify(json["password"], user.password_hash)):
                db.session.delete(user)
                db.session.commit()
                return {'status': 200, 'message': 'User was deleted successfully'}
            else:     
                return make_response(jsonify({'status': 400, 'message': 'Password has some wrong'}), 400)
        except:
            return {'status': 400, 'message': 'Request failed. Please try again'}
    if (request.method == 'PATCH'):
        try:
            user = Users.query.get(param)
            json = request.json
            print(json)
            for key in list(json.keys()):
                if (key == 'name'):
                    user.name = json['name']
                if (key == 'color'):
                    color = json['color']
                    user.r = color['r']
                    user.g = color['g']
                    user.b = color['b']
                    user.a = color['a']
                if (key == 'screen'):
                    user.df_screen = json['screen']
            db.session.add(user)
            db.session.commit()
            return {'status': 200, 'message': 'User was updated successfully'}
        except:
            return {'status': 400, 'message': 'Request fail. Please try again'}
