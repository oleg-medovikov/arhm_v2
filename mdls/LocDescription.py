from base import db
from datetime import datetime


class LocDescription(db.Model):
    __tablename__ = "loc_description"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.SmallInteger, primary_key=True)
    loc_id = db.Column(db.SmallInteger, db.ForeignKey("location.id"))
    profession = db.Column(db.String)
    stage = db.Column(db.SmallInteger)
    description = db.Column(db.String)
    image_id = db.Column(db.SmallInteger, db.ForeignKey("image.id"), nullable=True)

    u_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date_update = db.Column(db.DateTime(), default=datetime.now())

    @property
    def location(self):
        """The location property."""
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

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
