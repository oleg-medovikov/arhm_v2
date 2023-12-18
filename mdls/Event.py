from base import db
from datetime import datetime


class Event(db.Model):
    __tablename__ = "event"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    stick_id = db.Column(db.SmallInteger(), db.ForeignKey("sticker.id"), nullable=True)
    single_use = db.Column(db.Boolean)
    waste_time = db.Column(db.SmallInteger)

    # если монстр, то какой
    monster = db.Column(db.SmallInteger, nullable=True)

    # если с проверкой, выбор choice тоже запихиваем в json
    demand = db.Column(db.JSON, nullable=True)
    mess_prise = db.Column(db.String, nullable=True)
    mess_punish = db.Column(db.String, nullable=True)
    prise = db.Column(db.JSON, nullable=True)
    punish = db.Column(db.JSON, nullable=True)

    u_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    date_update = db.Column(db.DateTime(), default=datetime.now())

    @property
    def user(self):
        return self._users

    @user.setter
    def user(self, value):
        self._users = value
