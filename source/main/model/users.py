from source import db
from sqlalchemy import Column,String,Integer,DateTime
from sqlalchemy.orm import relationship


import datetime
import jwt
from sqlalchemy.sql import func
from source import app
class Users(db.Model):
    __tablename__ = 'users'
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(50))
    gmail=Column(String(70))
    user_name=Column(String(50))
    password_hash=Column(String(500),nullable=False)
    notes=relationship('Notes',backref='users',lazy=True, cascade="all, delete")
    df_color=Column(String(20),default="#FD8E8E")
    df_screen=Column(String(20),default="Archived")
    df_fontsize=Column(String(20),default="Default")
    
    createAt=Column(DateTime(timezone=True),default=func.now())
    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e
        
    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
    
   