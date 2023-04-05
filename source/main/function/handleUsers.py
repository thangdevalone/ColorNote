from source import db
from source.main.model.users import Users
from flask import request


def handleUsers(param):
    if (request.method == 'GET'):
        User = Users.query.get(param)

        return {'user': {'id': User.id, 'name': User.name, 'gmail': User.gmail, 'df_color': {'r': User.r,
                                                                                             'g': User.g, 'b': User.b, 'a': User.a},
                         'df_screen': User.df_screen}}
    if (request.method == 'DELETE'):
        try:
            user = Users.query.get(param)
            db.session.delete(user)
            db.session.commit()
            return {'status': 200, 'message': 'User was deleted successfully'}
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
