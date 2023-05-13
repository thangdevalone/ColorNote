from source import db
from source.main.model.users import Users
from source.main.model.notes import Notes
from source.main.model.datas import Datas
from source.main.model.groups import Groups
from source.main.model.chats import Chats
from source.main.model.members import Members


if __name__ == "__main__":
    db.create_all()