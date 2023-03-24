from source import db
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from source.main.model.users import Users
from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

class Notes(db.Model):
    __tablename__ = 'notes'
    idNote = Column(Integer, primary_key=True, autoincrement=True)
    idUser = Column(Integer, ForeignKey(Users.id), nullable=False)
    type = Column(String(20), nullable=False)
    title = Column(String(50), nullable=False)
    pinned = Column(Boolean, nullable=False, default=0)
    dueAt = Column(DateTime(timezone=True), nullable=False)
    color = Column(String(20), nullable=False)
    remindAt=Column(DateTime(timezone=True))
    doneNote=Column(Boolean, nullable=False, default=0)
    createAt=Column(DateTime(timezone=True),default=func.now())
    datas=relationship('Datas',backref='notes',lazy=True, cascade="all, delete")

   
        