from source import app
from source.main.controller.notes import *
from source.main.controller.users import *


@app.route('/')
def reader():
    return '<a href="/docs">/docs</a> to read the documentation'

