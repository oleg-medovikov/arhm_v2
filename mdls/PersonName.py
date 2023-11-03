from base import db
from datetime import datetime


class PersonName(db.Model):
    __tablename__ = "person_name"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.SmallInteger(), primary_key=True)
    gamename = db.Column(db.String(length=50))
    profession = db.Column(db.String(length=20))

    u_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    date_update = db.Column(db.DateTime(), default=datetime.now())

    @property
    def user(self):
        return self._users

    @user.setter
    def user(self, value):
        self._users = value
