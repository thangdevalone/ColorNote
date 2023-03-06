from source import db
from source.main.model.users import Users
from flask import request

def handleUsers(param):
    if (request.method == 'GET'):
        user=Users.query.get(param)
        user_parse=user.__dict__
        user_parse.pop('_sa_instance_state')
        return {"user": user_parse}
    if (request.method == 'DELETE'):
        try:
            user=Users.query.get(param)
            db.session.delete(user)
            db.session.commit()
            return {'status': 200, 'message': 'User was deleted successfully'}
        except:
             return {'status': 400, 'message': 'Request failed. Please try again'}
    if (request.method == 'PATCH'):
        try:
            user=Users.query.get(param)
            json = request.json
            print(json)
            for key in list(json.keys()):
                if(key=='name'):
                    user.name = json['name']
                if(key=='gmail'):
                    user.gmail = json['gmail']
            db.session.add(user)
            db.session.commit()
            return {'status': 200, 'message': 'User was updated successfully'}
        except:
            return {'status': 400, 'message': 'Request fail. Please try again'}