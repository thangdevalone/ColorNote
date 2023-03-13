from source import app,mail
from source.main.function.handleUsers import handleUsers
from source.main.function.createUser import createUser
from source.main.function.getAllUsers import getAllUsers
from source.main.function.loginUser import loginUser
from flask import request,url_for
from itsdangerous import URLSafeTimedSerializer
from flask_mail import *
from source.main.model.users import Users
s=URLSafeTimedSerializer(app.config["SECRET_KEY"])

app.add_url_rule('/user/<string:param>',methods=['GET','PATCH','DELETE'],view_func=handleUsers)
app.add_url_rule('/allUsers',methods=['GET'],view_func=getAllUsers)
app.add_url_rule('/login',methods=['POST'],view_func=loginUser)


@app.route('/register',methods=["GET","POST"])
def verifylink():
    try:
        json=request.json
        if (bool(json)):
            user= Users.query.filter(Users.user_name == json["user_name"]).first()
            if(not user):
                token=s.dumps(json,salt=app.config["SECURITY_PASSWORD_SALT"])
                msg=Message('Confirmation',sender="quangthanghocmai3@gmail.com",recipients=[json['gmail']])
                link=url_for('confirm',token=token,_external=True)
                msg.body="your confirmation link is " +link
                mail.send(msg)
                return "Please check your email or spam"
            else:
                return {'status': 400, 'message': 'Account already exists'}
        else:
            return {'status':400,'message':"Request fail. Please try again"}
    except:
        return {'status':400,'message':"Request fail. Please try again"}
@app.route('/confirm/<token>')
def confirm(token):
    try:
        json=s.loads(token,salt=app.config["SECURITY_PASSWORD_SALT"],max_age=3600)
        createUser(json)
    except:
        return {"status":400,"message":"Link expired. Please try again"}
    
    return {"status":200,"message":"Your account was created successfully. Please try login"}