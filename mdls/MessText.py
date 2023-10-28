from base import db
from datetime import datetime


class MessText(db.Model):
    __tablename__ = "mess_text"

    name = db.Column(db.String(), primary_key=True)
    text = db.Column(db.String())
    date_update = db.Column(db.DateTime(), default=datetime.now())
