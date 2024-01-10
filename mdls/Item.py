from base import db
from datetime import datetime


class Item(db.Model):
    __tablename__ = "item"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.SmallInteger(), primary_key=True)
    name = db.Column(db.String(length=40))
    image_id = db.Column(db.SmallInteger(), db.ForeignKey("image.id"), nullable=True)
    description = db.Column(db.String())
    mess_equip = db.Column(db.String(), nullable=True)
    mess_equip_fail = db.Column(db.String(), nullable=True)
    mess_remove = db.Column(db.String(), nullable=True)
    mess_remove_fail = db.Column(db.String(), nullable=True)
    mess_drop = db.Column(db.String(), nullable=True)
    type_kind = db.Column(db.String(length=30))
    slot = db.Column(db.String(length=30))
    emoji = db.Column(db.String(length=30))
    effect = db.Column(db.JSON(), nullable=True)
    demand = db.Column(db.JSON(), nullable=True)
    cost = db.Column(db.SmallInteger(), nullable=True)
    alternative = db.Column(db.SmallInteger(), nullable=True)
    single_use = db.Column(db.Boolean())
    achievement = db.Column(db.Boolean())

    u_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    date_update = db.Column(db.DateTime(), default=datetime.now())

    @property
    def image(self):
        """The image property."""
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def user(self):
        return self._users

    @user.setter
    def user(self, value):
        self._users = value
