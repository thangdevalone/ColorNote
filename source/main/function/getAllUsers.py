from source.main.model.users import Users


def getAllUsers():
    users = Users.query.all()
    data = []
    for user in users:
        user_parse=user.__dict__
        user_parse.pop('_sa_instance_state')
        data.append(user_parse)
    return {"users": data}
