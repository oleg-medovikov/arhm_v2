from base import db
from datetime import datetime


class Monster(db.Model):
    __tablename__ = "monster"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String(length=40))
    stick_id = db.Column(db.SmallInteger, db.ForeignKey("sticker.id"), nullable=True)
    description = db.Column(db.String)
    mess_win = db.Column(db.String)
    mess_lose_hp = db.Column(db.String)
    mess_lose_md = db.Column(db.String)
    check_stels = db.Column(db.SmallInteger)
    nightmare = db.Column(db.SmallInteger)
    crush = db.Column(db.SmallInteger)
    phisical_resist = db.Column(db.SmallInteger)
    magical_resist = db.Column(db.SmallInteger)
    check_mind = db.Column(db.SmallInteger)
    check_fight = db.Column(db.SmallInteger)
    damage_mind = db.Column(db.SmallInteger)
    damage_body = db.Column(db.SmallInteger)
    health = db.Column(db.SmallInteger)
    price = db.Column(db.SmallInteger)
    item = db.Column(db.ARRAY(db.SmallInteger))
    expirience = db.Column(db.SmallInteger)

    u_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date_update = db.Column(db.DateTime, default=datetime.now())

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
