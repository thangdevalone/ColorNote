from source import app
from source.main.function.getAllNotes import getAllNotes
from source.main.function.handleNotes import handleNotes

app.add_url_rule('/allNotes', methods=['GET'], view_func=getAllNotes)
app.add_url_rule('/notes/<string:param>',
                 methods=['GET', 'POST', "PATCH", "DELETE"], view_func=handleNotes)

