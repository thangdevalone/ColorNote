from source import db
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from source.main.model.users import Users


class Notes(db.Model):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    idUser = Column(Integer, ForeignKey(Users.id), nullable=False)
    type = Column(String(20), nullable=False)
    title = Column(String(50), nullable=False)
    data = Column(String(500))
    pinned = Column(Boolean, nullable=False, default=0)
    date = Column(DateTime, nullable=False)
    color = Column(String(20), nullable=False)

   
        