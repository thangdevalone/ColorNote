
from flask_socketio import emit,join_room,leave_room
from flask import request
from source import socketIo,db,connected_clients
from source.main.model.chats import Chats
from datetime import datetime


@socketIo.on('online')
def online(data):
    fl=True
    print('client connect')
    for obj in connected_clients:
        if obj.get('id') == data['user']['id']:
            fl=False
            break
    if(fl==True):
        connected_clients.append(data['user'])
    print(connected_clients)
    # Gửi danh sách client đang kết nối cho client vừa kết nối thành công
    emit('online', {'online':connected_clients})
@socketIo.on('offline')
def offline(client_id ):
    print(f'user :{client_id}')
    print('client offline')
    for obj in connected_clients:
        if obj.get('id') == client_id:
            connected_clients.remove(obj)
            print(connected_clients)
            break
    
    
    # Gửi danh sách client đang kết nối cho client vừa kết nối thành công
    emit('offline', {'online':connected_clients})
@socketIo.on('connect')
def connected():
   
    client_id = request.sid
    
    print(connected_clients)
    emit('connect',  {'online':connected_clients})
    


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
    
