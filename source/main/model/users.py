from source import db
from sqlalchemy import Column,String,Integer
from sqlalchemy.orm import relationship

class Users(db.Model):
    __tablename__ = 'users'
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(50))
    gmail=Column(String(70))
    notes=relationship('Notes',backref='users',lazy=True)
    
   