from source import db
from source.main.model.users import Users
from source.main.model.notes import Notes

if __name__ == "__main__":
    db.create_all()