from base import db


class PersonNote(db.Model):
    __tablename__ = "person_note"
    __table_args__ = {"extend_existing": True}

    p_id = db.Column(db.SmallInteger(), db.ForeignKey("person.id"))
    gametime = db.Column(db.SmallInteger())
    n_id = db.Column(db.SmallInteger(), db.ForeignKey("note_text.id"))

    @property
    def person(self):
        return self._person

    @person.setter
    def person(self, value):
        self._person = value

    @property
    def note_text(self):
        """The note_text property."""
        return self._note_text

    @note_text.setter
    def note_text(self, value):
        self._note_text = value
