from base import db
from datetime import datetime


class Item(db.Model):
    __tablename__ = "item"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.SmallInteger(), primary_key=True)
    name = db.Column(db.String(length=40))
    sticker = db.Column(db.SmallInteger(), db.ForeignKey("sticker.id"), nullable=True)
    description = db.Column(db.String())
    mess_equip = db.Column(db.String(), nullable=True)
    mess_fail = db.Column(db.String(), nullable=True)
    mess_remove = db.Column(db.String(), nullable=True)
    mess_drop = db.Column(db.String(), nullable=True)
    type_kind = db.Column(db.String(length=30))
    slot = db.Column(db.String(length=30))
    emoji = db.Column(db.String(length=30))
    effect = db.Column(db.JSON(), nullable=True)
    demand = db.Column(db.JSON(), nullable=True)
    cost = db.Column(db.SmallInteger(), nullable=True)
    single_use = db.Column(db.Boolean())
    achievement = db.Column(db.Boolean())

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
