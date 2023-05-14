from source import db, app
from source.main.model.groups import Groups
from source.main.model.members import Members
from source.main.model.chats import Chats
from source.main.model.users import Users


from flask_jwt_extended import jwt_required
from flask import request, make_response, jsonify
from sqlalchemy import text, and_
import jwt


def handleNotesGroup(idNote):
    pass


def createGroup(owner):
    try:
        json = request.json

        groupFilter = Groups.query.filter(
            and_(Groups.idOwner == owner, Groups.name == json["name_group"])).first()
        if (groupFilter):
            return make_response(jsonify({'status': 200, 'message': 'Group name was exist'}), 400)
        else:
            group = Groups(
                name=json["name_group"], idOwner=owner, describe=json["describe_group"])
            db.session.add(group)
            db.session.commit()
            for mem in json["members"]:
                member = Members(idGroup=group.idGroup,
                                 idUser=mem['id'], role=mem["role"])
                db.session.add(member)
            db.session.commit()
            group_if = {}
            group_if['idGroup'] = group.idGroup
            tv = db.session.execute(text(
                'select count(idMember) as thanh_vien from members as m where m.idGroup={}'.format(group.idGroup)))
            for row in tv:
                group_if['numberMems'] = row.thanh_vien
            group_if['name'] = group.name

            group_if['createAt'] = str(group.createAt)
            group_if['idOwner'] = group.idOwner
            group_if['describe'] = group.describe
            return {'status': 200, 'message': 'Group was created successfully', 'group': group_if}
    except:
        return make_response(jsonify({'status': 400, 'message': 'Request fail. Please try again'}), 400)


def addMembers(idGr):
    try:
        json = request.json

        def getIdUser(user):
            return {"id": user.id, "role": user["role"]}
        memberId = map(getIdUser, json["member"])
        for mem in memberId:
            member = Members(idGroup=idGr, idUser=mem.id, role=mem.role)
            db.session.add(member)
        db.session.commit()
        return {'status': 200, 'message': 'Member was added successfully'}
    except:
        return make_response(jsonify({'status': 400, 'message': 'Request fail. Please try again'}), 400)


def quitMembers():
    pass


def getAllGroup(user):
    if (request.method == 'GET'):
        groups = db.session.execute(text(
            'Select * from members as m inner join `groups` as g on m.idGroup=g.idGroup where m.idUser={}'.format(user)))
        data = []
        for group in groups:
            group_if = {}
            group_if['idGroup'] = group.idGroup
            tv = db.session.execute(text(
                'select count(idMember) as thanh_vien from members as m where m.idGroup={}'.format(group.idGroup)))
            for row in tv:
                group_if['numberMems'] = row.thanh_vien
            group_if['name'] = group.name

            group_if['createAt'] = str(group.createAt)
            group_if['idOwner'] = group.idOwner
            group_if['describe'] = group.describe
            data.append(group_if)
        return {'status': 200, 'data': data}


def getGroup(id):
    if (request.method == 'GET'):
        group = Groups.query.filter(Groups.idGroup == id).first()
        group_if = {}
        group_if['idGroup'] = group.idGroup
        group_mems_avt = []
        group_if['members'] = []
        tv = db.session.execute(text(
            'select *  from members as m inner join users as u on m.idUser=u.id where m.idGroup={}'.format(group.idGroup)))
        for row in tv:

            member_if = {}
            member_if['avt'] = row.linkAvatar
            member_if['name'] = row.name
            member_if['id'] = row.id
            member_if['role'] = row.role
            group_if['members'].append(member_if)
            group_mems_avt.append(row.linkAvatar)
        group_if['avt'] = {'avt': group.linkAvatar, 'mems': group_mems_avt}
        group_if['name'] = group.name
        group_if['createAt'] = str(group.createAt)
        group_if['idOwner'] = group.idOwner
        group_if['describe'] = group.describe
        return {'status': 200, 'data': group_if}


def getMessages(id):
    if (request.method == 'GET'):
        chats = Chats.query.filter_by(
            idGroup=id).order_by(Chats.sendAt.desc()).all()
        data = []
        for chat in chats:
            chat_parse = {}
            chat_parse["id"] = chat.idMes
            chat_parse["type"] = chat.type
            chat_parse["idSend"] = chat.idSend
            user = Users.query.filter_by(id=chat.idSend).first()
            chat_parse["avt"] = user.linkAvatar
            chat_parse["name"] = user.name
            if (chat.type == "image" or chat.type == "muti-image" or chat.type == "icon-image"):
                chat_parse['metaData'] = chat.image
            else:
                chat_parse['content'] = chat.text
            chat_parse['sendAt'] = str(chat.sendAt)
            data.append(chat_parse)
    return {'status': 200, 'data': data}


def getImages(id):
    if (request.method == 'GET'):
        images = db.session.execute(text(
            f'select * from chats as c inner join users as u on c.idSend=u.id  where idGroup={id} and (type="image" or type="muti-image")'))
        images_by_date = {}
        show=[]
        idx=1
        for image in images:
            # Lấy ngày từ trường 'created_at' của tin nhắn
            date = image.sendAt.strftime('%d-%m-%y')
            
            # Kiểm tra xem ngày đã được lưu trong dict chưa
            if date not in images_by_date:
                # Nếu chưa, tạo một dict mới cho ngày này và lưu trữ các hình ảnh vào dict
                images_by_date[date] = {'date': date, 'images': []}
            
            # Lưu trữ thông tin của hình ảnh trong dict của ngày tương ứng
            if(image.type=="image"):
                image_info = {
                    'id': idx,
                    'url': image.image,
                    'idSend':image.idSend,
                    'name':image.name,
                    'type': "image",
                    'sendAt': str(image.sendAt)
                }
                images_by_date[date]['images'].append(image_info)
                if(len(show)<=8):
                    show.append(image_info)
                idx+=1
            else:
                arr_image=image.image.split(";")
                for i in arr_image:
                    image_info = {
                        'id': idx,
                        'url': i,
                        'idSend':image.idSend,
                        'name':image.name,
                        'type': "image",
                        'sendAt': str(image.sendAt)
                    }
                    idx+=1
                    if(len(show)<=8):
                        show.append(image_info)
                    images_by_date[date]['images'].append(image_info)
                
        image_list = [images_by_date[date] for date in images_by_date]
    return {'status': 200, 'images': image_list,'show':show}
