from source import app

from source.main.function.handleGroups import *

app.add_url_rule('/group',
                 methods=['GET', 'POST', "PATCH", "DELETE"], view_func=handleNotesGroup)
app.add_url_rule('/group/create/<string:owner>',
                 methods=['POST'], view_func=createGroup)
app.add_url_rule('/group/all/<string:user>',
                 methods=['GET'], view_func=getAllGroup)
app.add_url_rule('/group/only/<string:id>',
                 methods=['GET'], view_func=getGroup)
app.add_url_rule('/group/add/<string:idGr>',
                 methods=['POST'], view_func=addMembers)
app.add_url_rule('/group/quit/<string>',
                 methods=['delete'], view_func=quitMembers)

app.add_url_rule('/group/messages/<string:id>',
                 methods=['get'], view_func=getMessages)
app.add_url_rule('/group/images/<string:id>',
                 methods=['get'], view_func=getImages)