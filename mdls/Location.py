from base import db
from datetime import datetime


class Location(db.Model):
    __tablename__ = "location"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.SmallInteger(), primary_key=True)
    name = db.Column(db.String(length=40))
    declension = db.Column(db.String(length=40))
    contact_list = db.Column(db.ARRAY(db.SmallInteger()))
    district = db.Column(db.String(length=20))
    district_id = db.Column(db.SmallInteger())

    u_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    date_update = db.Column(db.DateTime(), default=datetime.now())

    @property
    def user(self):
        return self._users

    @user.setter
    def user(self, value):
        self._users = value
