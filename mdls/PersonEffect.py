from base import db
from datetime import datetime


class PersonEffect(db.Model):
    __tablename__ = "person_effect"
    __table_args__ = {"extend_existing": True}

    time = db.Column(db.DateTime, default=datetime.now(), primary_key=True)
    p_id = db.Column(db.SmallInteger, db.ForeignKey("person.id"))
    e_id = db.Column(db.SmallInteger, db.ForeignKey("effect.id"))
    gametime_start = db.Column(db.SmallInteger)
    gametime_stop = db.Column(db.SmallInteger)
    active = db.Column(db.Boolean, default=True)
