
from sqlalchemy import text
from source.main.model.notes import Notes
from source.main.model.datas import Datas

from flask import jsonify, make_response, request
from datetime import datetime,timezone
from source import db

def getNotes(param):
    notes = db.session.execute(text('Select * from (select * from notes where notes.idUser={}) as b inner join datas on b.idNote=datas.idNote'.format(param)))
    data = []
    for note in notes:
        note_parse={}
        if(note.type=='checklist'):
            flag=False
            if(len(data)>0):
                for item in data:
                    
                    if( item['type']=='checklist' and item['idNote']==note.idNote):
                        flag=True
                        item['data'].append({'content':note.content,'status':note.doneContent,'id':note.idData})
            if(flag==False):
                note_parse["idNote"]=note.idNote
                note_parse["type"]=note.type
                note_parse["data"]=[{'content':note.content,'status':note.doneContent,'id':note.idData}]
                note_parse["title"]=note.title
                note_parse["doneNote"]=note.doneNote
                note_parse["createAt"]=str(note.createAt)
                note_parse["dueAt"]=note.dueAt
                note_parse["pinned"]=note.pinned
                note_parse["idUser"]=note.idUser
                note_parse["color"]=note.color
        if(note.type=='text'):
            note_parse["idNote"]=note.idNote
            note_parse["type"]=note.type
            note_parse["data"]=note.content
            note_parse["title"]=note.title
            note_parse["doneNote"]=note.doneNote
            note_parse["createAt"]=str(note.createAt)
            note_parse["dueAt"]=str(note.dueAt)
            note_parse["pinned"]=note.pinned
            note_parse["idUser"]=note.idUser
            note_parse["color"]=note.color
            
                    
        if (bool(note_parse)): 
            data.append(note_parse)
    return data

def getNote(param):
    notes = db.session.execute(text('Select * from (select * from notes where notes.idNote={}) as b inner join datas on b.idNote=datas.idNote'.format(param)))
    note_parse={}
   
    flag=False
    
    for note in notes:
        if(note.type=='checklist'):
            if(flag==False):
                flag=True
                note_parse["idNote"]=note.idNote
                note_parse["type"]=note.type
                note_parse["data"]=[]
                note_parse["title"]=note.title
                note_parse["doneNote"]=note.doneNote
                note_parse["createAt"]=str(note.createAt)
                note_parse["dueAt"]=str(note.dueAt)
                note_parse["pinned"]=note.pinned
                note_parse["idUser"]=note.idUser
                note_parse["color"]=note.color
            if(flag==True):
                note_parse["data"].append({'content':note.content,'status':note.doneContent,'id':note.idData})

            
        if(note.type=='text'):
            note_parse["idNote"]=note.idNote
            note_parse["type"]=note.type
            note_parse["data"]=note.content
            note_parse["title"]=note.title
            note_parse["doneNote"]=note.doneNote
            note_parse["createAt"]=str(note.createAt)
            note_parse["dueAt"]=str(note.dueAt)
            note_parse["pinned"]=note.pinned
            note_parse["idUser"]=note.idUser
            note_parse["color"]=note.color
            
                    
        
    return note_parse
def handleNotes(param):
    if (request.method == "GET"):
        
        return {"notes": getNotes(param)}

    if (request.method == "POST"):
        # try:
        json = request.json
        note = Notes(idUser=param, type=json['type'], title=json['title'],pinned=json['pinned'], dueAt=datetime.strptime(json['dueAt'],"%d/%m/%Y %H:%M %p %z"), color=json['color'])
        db.session.add(note)
        
        db.session.commit()
        if(json['type']=='checklist'):
            for each in json['data']:
                data=Datas(idNote=note.idNote,content=each)
                db.session.add(data)
        else:   
            data=Datas(idNote=note.idNote,content=json['data'])
            db.session.add(data)
        db.session.commit()
        return {'status': 200, 'message': 'Note was created successfully','note':getNote(note.idNote)}
        # except:
        #     return make_response(jsonify({'status': 400, 'message': 'Request fail. Please try again'}),400)
       

    if (request.method == "PATCH"):
        try:
            json = request.json
            note_query = Notes.query.get(param)
            for key in list(json.keys()):
                if(key=='date'):
                    note_query.date = datetime.strptime(json['date'],"%d/%m/%Y %H:%M")
                if(key=='color'):
                    note_query.color = json['color']
                if(key=='data'):
                    note_query.data = json['data']
                if(key=='pinned'):
                    note_query.pinned = json['pinned']
            
            db.session.add(note_query)
            db.session.commit()
            return {'status': 200, 'message': 'Note was updated successfully'}
        except:
                return make_response(jsonify({'status': 400, 'message': 'Request fail. Please try again'}),400)
    if (request.method== 'DELETE'):
        try:
            note_query=db.session.query(Notes).filter_by(idNote=param).first()
            print(note_query)
            db.session.delete(note_query)
            db.session.commit()
            return {'status': 200, 'message': 'Note was deleted successfully'}
        except:
             return make_response(jsonify({'status': 400, 'message': 'Request fail. Please try again'}),400)
            
        
       
            
            