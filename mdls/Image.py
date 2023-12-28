from base import db
from datetime import datetime


class Image(db.Model):
    __tablename__ = "image"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    file_id = db.Column(db.String)
    file = db.Column(db.LargeBinary)

    u_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    date_update = db.Column(db.DateTime(), default=datetime.now())

    @property
    def user(self):
        return self._users

    @user.setter
    def user(self, value):
        self._users = value
