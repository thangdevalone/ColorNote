from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_mail import *
app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"]="devsenior"
app.config["SECURITY_PASSWORD_SALT"]="devsenior"
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:123456@localhost/colornote?charset=utf8"
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS']=True
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']="quangthanghocmai3@gmail.com"
app.config['MAIL_PASSWORD']="misoqnvbknqcslia"
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
app.app_context().push()
mail=Mail(app)
db=SQLAlchemy(app)
