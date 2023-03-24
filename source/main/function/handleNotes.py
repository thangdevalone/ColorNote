
from sqlalchemy import text
from source.main.model.notes import Notes
from source.main.model.datas import Datas

from flask import jsonify, make_response, request
from datetime import datetime
from source import db


def handleNotes(param):
    if (request.method == "GET"):
        notes = db.session.execute(text('Select * from (select * from notes where notes.idUser={}) as b inner join datas on b.idNote=datas.idNote'.format(param)))
        data = []
        for note in notes:
            note_parse={}
            if(note.type=='checklist'):
                flag=False
                if(len(data)>0):
                    for item in data:
                        print(item)
                        if( item['type']=='checklist' and item['idNote']==note.idNote):
                            flag=True
                            item['data'].append({'content':note.content,'status':note.doneContent})
                if(flag==False):
                    note_parse["idNote"]=note.idNote
                    note_parse["type"]=note.type
                    note_parse["data"]=[{'content':note.content,'status':note.doneContent}]
                    note_parse["title"]=note.title
                    note_parse["doneNote"]=note.doneNote
                    note_parse["createAt"]=note.createAt
                    note_parse["dueAt"]=note.dueAt
                    note_parse["pinned"]=note.pinned
                    note_parse["idUser"]=note.idUser
            if(note.type=='text'):
                note_parse["idNote"]=note.idNote
                note_parse["type"]=note.type
                note_parse["data"]=note.content
                note_parse["title"]=note.title
                note_parse["doneNote"]=note.doneNote
                note_parse["createAt"]=note.createAt
                note_parse["dueAt"]=note.dueAt
                note_parse["pinned"]=note.pinned
                note_parse["idUser"]=note.idUser
                        
            if (bool(note_parse)): 
                data.append(note_parse)
        return {"notes": data}

    if (request.method == "POST"):
        try:
            json = request.json
            note = Notes(idUser=param, type=json['type'], title=json['title'],pinned=json['pinned'], dueAt=datetime.strptime(json['date'],"%d/%m/%Y %H:%M:%S GMT%z"), color=json['color'])
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
            return {'status': 200, 'message': 'Note was created successfully'}
        except:
            return make_response(jsonify({'status': 400, 'message': 'Request fail. Please try again'}),400)
       

    if (request.method == "PATCH"):
        try:
            json = request.json
            note_query = Notes.query.get(param)
            for key in list(json.keys()):
                if(key=='date'):
                    note_query.date = datetime.strptime(json['date'],"%d/%m/%Y %H:%M:%S")
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
            
        
       
            
            