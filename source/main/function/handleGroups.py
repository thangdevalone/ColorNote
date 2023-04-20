from source import db
from source.main.model.groups import Groups
from source.main.model.members import Members

from flask import request,make_response,jsonify
from source.verify_token import *

@token_required
def handleNotesGroup(idNote):
    pass
@token_required
def createGroup():
    try:
        json = request.json
        group=Groups(idGroup=json["id"],name=json["name"],describe=json["describe"])
        db.session.add(group)
        db.session.commit()
        return {'status': 200, 'message': 'Group was created successfully'}
    except:
        return make_response(jsonify({'status': 400, 'message': 'Request fail. Please try again'}), 400)
@token_required
def addMembers(idGr):
    try:
        json = request.json
        def getIdUser(user):
            userFind=Users.query.filter(Users.gmail==user.gmail)
            return {"id":userFind.id,"role":user["role"]}
        memberId=map(getIdUser,json["member"])
        for mem in memberId:
            member=Members(idGroup=idGr,idUser=mem.id,role=mem.role)
            db.session.add(member)
        db.session.commit()
        return {'status': 200, 'message': 'Member was added successfully'}
    except:
        return make_response(jsonify({'status': 400, 'message': 'Request fail. Please try again'}), 400)

@token_required
def quitMembers():
    pass