from source import app,mail
from source.main.function.handleUsers import handleUsers
from source.main.function.createUser import createUser
from source.main.function.getAllUsers import getAllUsers
from source.main.function.loginUser import loginUser
from flask import jsonify, make_response, request,url_for,redirect
from itsdangerous import URLSafeTimedSerializer
from flask_mail import *
from source.main.model.users import Users
s=URLSafeTimedSerializer(app.config["SECRET_KEY"])
import webbrowser
app.add_url_rule('/user/<string:param>',methods=['GET','PATCH','DELETE'],view_func=handleUsers)
app.add_url_rule('/allUsers',methods=['GET'],view_func=getAllUsers)
app.add_url_rule('/login',methods=['POST'],view_func=loginUser)


@app.route('/register',methods=["GET","POST"])
def verifylink():
    try:
        json=request.json
        print(json)
        if (bool(json)):
            user= Users.query.filter(Users.user_name == json["user_name"]).first()
            print(user)
            if(not user):
                token=s.dumps(json,salt=app.config["SECURITY_PASSWORD_SALT"])
                msg=Message('Confirmation',sender="quangthanghocmai3@gmail.com",recipients=[json['gmail']])
                link=url_for('confirm',token=token,_external=True)
                msg.body="Your confirmation link is " +link
                mail.send(msg)
                return {'status': 200, 'message': "Please check your email or spam"}
            else:
                return  make_response(jsonify({'status': 400, 'message': 'Account already exists'}),400)
        else:
            return  make_response(jsonify({'status': 400, 'message': 'Request fail. Please try again'}),400)
    except: 
        return make_response(jsonify({'status': 400, 'message': 'Server had some problem. Please try again after 24h'}),400)
@app.route('/confirm/<token>')
def confirm(token):
    try:
        json=s.loads(token,salt=app.config["SECURITY_PASSWORD_SALT"],max_age=3600)
        createUser(json)
    except:
        return "Your link was expired. Try again"
    
    return redirect("https://www.facebook.com/")