from base import db
from datetime import datetime


class Dialog(db.Model):
    __tablename__ = "dialog"
    __table_args__ = {"extend_existing": True}

    d_id = db.Column(db.SmallInteger)
    q_id = db.Column(db.String)
    stick_id = db.Column(db.SmallInteger(), db.ForeignKey("sticker.id"), nullable=True)
    name = db.Column(db.String)
    question = db.Column(db.String)
    answers = db.Column(db.ARRAY(db.String))
    transfer = db.Column(db.ARRAY(db.String))
    demand = db.Column(db.JSON, nullable=True)
    spend_time = db.Column(db.SmallInteger, nullable=True)
    buy_items = db.Column(db.ARRAY(db.SmallInteger), nullable=True)
    buy_costs = db.Column(db.ARRAY(db.SmallInteger), nullable=True)
    sale_items = db.Column(db.ARRAY(db.SmallInteger), nullable=True)
    sale_costs = db.Column(db.ARRAY(db.SmallInteger), nullable=True)

    u_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    date_update = db.Column(db.DateTime(), default=datetime.now())

    @property
    def sticker(self):
        """The sticker property."""
        return self._sticker

    @sticker.setter
    def sticker(self, value):
        self._sticker = value

    @property
    def user(self):
        return self._users

    @user.setter
    def user(self, value):
        self._users = value
