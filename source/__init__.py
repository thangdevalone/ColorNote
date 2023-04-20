from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_mail import *
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO,send

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"]="devsenior"
app.config["SECURITY_PASSWORD_SALT"]="devsenior"
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:123456@localhost/colornote?charset=utf8"
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS']=True
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']="devseniorpro99@gmail.com"
app.config['MAIL_PASSWORD']="uqecxhjyqkwvoffd"
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

jwt=JWTManager(app)
app.app_context().push()
mail=Mail(app)
db=SQLAlchemy(app)
socketIo=SocketIO(app,cor_allow_origin="*")

