from base import db


class NoteText(db.Model):
    __tablename__ = "note_text"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.SmallInteger(), primary_key=True)
    text = db.Column(db.String())
