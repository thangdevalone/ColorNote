
from sqlalchemy import text
from source.main.model.notes import Notes
from source.main.model.datas import Datas

from flask import jsonify, make_response, request
from datetime import datetime, timezone
from source import db


def getNotes(notes):
    data = []
    for note in notes:
        note_parse = {}
        if (note.type == 'checklist'):
            flag = False
            if (len(data) > 0):
                for item in data:

                    if (item['type'] == 'checklist' and item['idNote'] == note.idNote):
                        flag = True
                        item['data'].append(
                            {'content': note.content, 'status': note.doneContent, 'id': note.idData})
            if (flag == False):
                note_parse["idNote"] = note.idNote
                note_parse["type"] = note.type
                note_parse["data"] = [
                    {'content': note.content, 'status': note.doneContent, 'id': note.idData}]
                note_parse["title"] = note.title
                note_parse["doneNote"] = note.doneNote
                note_parse["createAt"] = str(note.createAt)
                note_parse["dueAt"] = note.dueAt
                note_parse["pinned"] = note.pinned
                note_parse["idUser"] = note.idUser
                note_parse["color"] = {'r': note.r,
                                       'g': note.g, 'b': note.b, 'a': note.a}
        if (note.type == 'text'):
            note_parse["idNote"] = note.idNote
            note_parse["type"] = note.type
            note_parse["data"] = note.content
            note_parse["title"] = note.title
            note_parse["doneNote"] = note.doneNote
            note_parse["createAt"] = str(note.createAt)
            note_parse["dueAt"] = str(note.dueAt)
            note_parse["pinned"] = note.pinned
            note_parse["idUser"] = note.idUser
            note_parse["color"] = {'r': note.r,
                                   'g': note.g, 'b': note.b, 'a': note.a}

        if (bool(note_parse)):
            data.append(note_parse)
    return data


def getNote(param):
    notes = db.session.execute(text(
        'Select * from (select * from notes where notes.idNote={}) as b inner join datas on b.idNote=datas.idNote'.format(param)))
    note_parse = {}

    flag = False

    for note in notes:
        if (note.type == 'checklist'):
            if (flag == False):
                flag = True
                note_parse["idNote"] = note.idNote
                note_parse["type"] = note.type
                note_parse["data"] = []
                note_parse["title"] = note.title
                note_parse["doneNote"] = note.doneNote
                note_parse["createAt"] = str(note.createAt)
                note_parse["dueAt"] = str(note.dueAt)
                note_parse["pinned"] = note.pinned
                note_parse["idUser"] = note.idUser
                note_parse["color"] = {'r': note.r,
                                       'g': note.g, 'b': note.b, 'a': note.a}
            if (flag == True):
                note_parse["data"].append(
                    {'content': note.content, 'status': note.doneContent, 'id': note.idData})

        if (note.type == 'text'):
            note_parse["idNote"] = note.idNote
            note_parse["type"] = note.type
            note_parse["data"] = note.content
            note_parse["title"] = note.title
            note_parse["doneNote"] = note.doneNote
            note_parse["createAt"] = str(note.createAt)
            note_parse["dueAt"] = str(note.dueAt)
            note_parse["pinned"] = note.pinned
            note_parse["idUser"] = note.idUser
            note_parse["color"] = {'r': note.r,
                                   'g': note.g, 'b': note.b, 'a': note.a}

    return note_parse


def handleNotes(param):
    if (request.method == "GET"):
        notes = db.session.execute(text(
            'Select * from (select * from notes where notes.idUser={} and notes.inArchived=1) as b inner join datas on b.idNote=datas.idNote'.format(param)))

        return {"notes": getNotes(notes)}

    if (request.method == "POST"):
        try:
            json = request.json
            print(json)
            color = json['color']
            note = Notes(idUser=param, type=json['type'], title=json['title'], pinned=json['pinned'], dueAt=datetime.strptime(
                json['dueAt'], "%d/%m/%Y %H:%M %p %z"), r=color['r'], g=color['g'], b=color['b'], a=color['a'])
            db.session.add(note)

            db.session.commit()
            if (json['type'] == 'checklist'):
                for each in json['data']:
                    data = Datas(idNote=note.idNote,
                                 content=each['content'], doneContent=each['status'])
                    db.session.add(data)
            else:
                data = Datas(idNote=note.idNote, content=json['data'])
                db.session.add(data)
            db.session.commit()
            return {'status': 200, 'message': 'Note was created successfully', 'note': getNote(note.idNote)}
        except:
            return make_response(jsonify({'status': 400, 'message': 'Request fail. Please try again'}), 400)
    if (request.method == "PATCH"):
        try:
            json = request.json
            note_query = Notes.query.get(param)
            for key in list(json.keys()):
                if (key == 'dueAt'):
                    note_query.date = datetime.strptime(
                        json['dueAt'], "%d/%m/%Y %H:%M %p %z")
                if (key == 'color'):
                    color = json['color']
                    note_query.r = color['r']
                    note_query.g = color['g']
                    note_query.b = color['b']
                    note_query.a = color['a']
                if(key=='title'):
                    note_query.title=json['title']
                if (key == 'data'):

                    if (json['type'] == 'text'):
                        note_data = Datas.query.filter(
                            Datas.idNote == param).first()

                        note_data.content = json['data']
                        db.session.add(note_data)

                    if (json['type'] == 'checklist'):
                        trunc_data = Datas.query.filter(
                                Datas.idNote == param).all()
                        for item in trunc_data:
                            db.session.delete(item)
                        db.session.commit()
                        for edit in json['data']:
                            data = Datas(idNote=param,
                                            content=edit['content'], doneContent=edit['status'])
                            db.session.add(data)
                        

                if (key == 'pinned'):
                    note_query.pinned = json['pinned']

            db.session.add(note_query)
            db.session.commit()
            return {'status': 200, 'message': 'Note was updated successfully', 'note': getNote(note_query.idNote)}
        except:
            return make_response(jsonify({'status': 400, 'message': 'Request fail. Please try again'}), 400)
    if (request.method == 'DELETE'):
        try:
            note_query = db.session.query(
                Notes).filter_by(idNote=param).first()
            note_query.inArchived = False
            db.session.add(note_query)
            db.session.commit()
            return {'status': 200, 'message': 'Note was deleted successfully', 'note': getNote(note_query.idNote)}
        except:
            return make_response(jsonify({'status': 400, 'message': 'Request fail. Please try again'}), 400)

def tickerBox(idData):
    if (request.method == 'PATCH'):
        # try:
            data=Datas.query.filter(Datas.idData==idData).first()
            data.doneContent=not data.doneContent
            db.session.add(data)
            db.session.commit()
            return {'status': 200, 'message': 'Note was update successfully'}
        # except:
        #     return make_response(jsonify({'status': 400, 'message': 'Request fail. Please try again'}), 400)

def delTruncNote(id):
    if (request.method == 'DELETE'):
        try:
            note_query = db.session.query(Notes).filter_by(idNote=id).first()
            print(note_query)
            db.session.delete(note_query)
            db.session.commit()
            return {'status': 200, 'message': 'Note was deleted successfully', }
        except:
            return make_response(jsonify({'status': 400, 'message': 'Request fail. Please try again'}), 400)


def trashGet(idUser):
    if (request.method == "GET"):
        notes = db.session.execute(text(
            'Select * from (select * from notes where notes.idUser={} and notes.inArchived=0) as b inner join datas on b.idNote=datas.idNote'.format(idUser)))

        return {"notes": getNotes(notes)}


def trashRestore(id):
    if (request.method == "POST"):
        try:
            note_query = db.session.query(Notes).filter_by(idNote=id).first()
            note_query.inArchived = True
            db.session.add(note_query)
            db.session.commit()
            return {'status': 200, 'message': 'Note was restore successfully', "note": getNote(note_query.idNote)}
        except:
            return make_response(jsonify({'status': 400, 'message': 'Request fail. Please try again'}), 400)
