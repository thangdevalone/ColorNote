from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:123456@localhost/colornote?charset=utf8"
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS']=True
app.app_context().push()
db=SQLAlchemy(app)
