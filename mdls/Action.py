from base import db
from datetime import datetime


class Action(db.Model):
    __tablename__ = "action"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.SmallInteger, primary_key=True)
    loc_id = db.Column(db.SmallInteger, db.ForeignKey("location.id"))
    name = db.Column(db.String)

    dialog = db.Column(db.SmallInteger, nullable=True)
    events = db.Column(db.ARRAY(db.SmallInteger), nullable=True)
    weights = db.Column(db.ARRAY(db.Float), nullable=True)

    demand = db.Column(db.JSON, nullable=True)
    profession = db.Column(db.String)
    stage = db.Column(db.SmallInteger)

    u_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    date_update = db.Column(db.DateTime(), default=datetime.now())

    @property
    def user(self):
        return self._users

    @user.setter
    def user(self, value):
        self._users = value
