from base import db
from datetime import datetime


class Effect(db.Model):
    __tablename__ = "effect"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String)

    impact = db.Column(db.JSON)
    time = db.Column(db.SmallInteger)

    u_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    date_update = db.Column(db.DateTime(), default=datetime.now())

    @property
    def user(self):
        return self._users

    @user.setter
    def user(self, value):
        self._users = value
