from base import db
from datetime import datetime


class MessText(db.Model):
    __tablename__ = "mess_text"
    __table_args__ = {"extend_existing": True}

    name = db.Column(db.String(), primary_key=True)
    text = db.Column(db.String())

    u_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    update = db.Column(db.DateTime(), default=datetime.now())
