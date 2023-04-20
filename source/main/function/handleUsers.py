from source import db,app
from source.main.model.users import Users
from flask import request,make_response,jsonify
from sqlalchemy import text
import jwt
from passlib.hash import pbkdf2_sha256
def handleUsers(param):
    
    if (request.method == 'POST'):
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

def getAllUser():
    if(request.method=="GET"):
        try:
            bearer = request.headers.get('Authorization')    # Bearer YourTokenHere
            token = bearer.split(' ')[1]
            decoded_data = jwt.decode(jwt=token,
                            key=app.config["SECRET_KEY"],
                            algorithms=["HS256"])
            who=decoded_data['sub']['id']
            print(decoded_data,who)
            users=db.session.execute(text("select u.gmail, u.id from users as u where u.id != {}".format(who)))
            data=[]
            for user in users:
                user_config={}
                user_config["gmail"]=user.gmail
                user_config["id"]=user.id
                data.append(user_config)
            return {'status': 200,'data':data}
                
        except:
            return make_response(jsonify({'status': 400, 'message': 'Request fail. Please try again'}), 400)