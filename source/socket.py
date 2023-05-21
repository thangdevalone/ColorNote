
from flask_socketio import emit,join_room,leave_room
from flask import request
from source import socketIo,db
from source.main.model.chats import Chats
from datetime import datetime

connected_clients = {}
@socketIo.on('online')
def online():
    emit('online', connected_clients)
@socketIo.on('connect')
def connected():
    user=request.args.get('user')
    client_id = request.sid
    client_info = {
        'session_id': client_id,
        'namespace': request.namespace,
        'request': request,
        'user': user
    }
    connected_clients[client_id] = client_info

    # Gửi danh sách client đang kết nối cho client vừa kết nối thành công
    emit('connect', connected_clients)


@socketIo.on('disconnected')
def disconnected():
    print('User disconnected')
    emit("disconnected", f"User {request.sid} is connected", broadcast=True)

@socketIo.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    print("join")


@socketIo.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    print("leave")

@socketIo.on('chat_group')
def chat_group(data):
    room=data['room']
    message = data['data']
    print(message,data)
    newChat=Chats(idGroup=room,sendAt=datetime.strptime(
                message['sendAt'], "%d/%m/%Y %H:%M %p %z"),idSend=message["idSend"],type=message['type'])
    if(newChat.type=="image" or newChat.type=="icon-image" or newChat.type=="muti-image"):
        newChat.image=message['metaData']
    else:
        newChat.text=message['content']
    db.session.add(newChat)
    db.session.commit()
    message['sendAt']=str(newChat.sendAt)
     # Lấy thời gian hiện tại

    emit('chat_group',message, room=room)
    
