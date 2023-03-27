from source import db
from sqlalchemy import Column, String, Integer, ForeignKey,Boolean
from source.main.model.notes import Notes

class Datas(db.Model):
    __tablename__ = 'datas'
    idData = Column(Integer, primary_key=True, autoincrement=True)
    idNote = Column(Integer, ForeignKey(Notes.idNote), nullable=False)
    content = Column(String(500))
    doneContent=Column(Boolean, nullable=False, default=0)

   