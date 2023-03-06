from source.main.model.notes import Notes


def getAllNotes():
    notes = Notes.query.all()
    data = []
    for note in notes:
        note_parse=note.__dict__
        note_parse.pop('_sa_instance_state')
        data.append(note_parse)
    return {"notes": data}
