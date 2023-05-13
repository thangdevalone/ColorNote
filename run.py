from source import socketIo,app
from source.socket import *

import source.main.controller



if __name__ == '__main__':
    socketIo.run(app)