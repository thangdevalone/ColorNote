from source import app
from source.main.function.handleUsers import handleUsers
from source.main.function.createUser import createUser
from source.main.function.getAllUsers import getAllUsers
from source.main.function.loginUser import loginUser



app.add_url_rule('/user/<string:param>',methods=['GET','PATCH','DELETE'],view_func=handleUsers)
app.add_url_rule('/create-user',methods=['POST'],view_func=createUser)
app.add_url_rule('/allUsers',methods=['GET'],view_func=getAllUsers)
app.add_url_rule('/login',methods=['POST'],view_func=loginUser)


