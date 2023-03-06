from source.main.model.notes import Notes
from flask import request
from datetime import datetime
from source import db


def handleNotes(param):
    if (request.method == "GET"):
        notes = Notes.query.filter(Notes.idUser == param).all()
        data = []
        for note in notes:
            note_parse = note.__dict__
            note_parse.pop('_sa_instance_state')
            data.append(note_parse)
        return {"notes": data}

    if (request.method == "POST"):
        try:
            json = request.json
            data = Notes(idUser=param, type=json['type'], pinned=json['pinned'],data=json['data'], date=datetime.strptime(json['date'],"%d/%m/%Y %H:%M:%S"), color=json['color'])
            db.session.add(data)
            db.session.commit()
            return {'status': 200, 'message': 'Note was created successfully'}
        except:
                return {'status': 400, 'message': 'Request fail. Please try again'}

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
                if(key=='type'):
                    note_query.type = json['type']
            
            db.session.add(note_query)
            db.session.commit()
            return {'status': 200, 'message': 'Note was updated successfully'}
        except:
                return {'status': 400, 'message': 'Request fail. Please try again'}
    if (request.method== 'DELETE'):
        try:
            note_query =Notes.query.get(param)
            db.session.delete(note_query)
            db.session.commit()
            return {'status': 200, 'message': 'Note was deleted successfully'}
        except:
            return {'status': 400, 'message': 'Request fail. Please try again'}
            
            