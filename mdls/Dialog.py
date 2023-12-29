from base import db
from datetime import datetime


class Dialog(db.Model):
    __tablename__ = "dialog"
    __table_args__ = {"extend_existing": True}

    d_id = db.Column(db.SmallInteger)
    q_id = db.Column(db.Integer)
    image_id = db.Column(db.SmallInteger(), db.ForeignKey("image.id"), nullable=True)
    name = db.Column(db.String)
    question = db.Column(db.String)
    answers = db.Column(db.ARRAY(db.String))
    transfer = db.Column(db.ARRAY(db.Integer))
    demand = db.Column(db.JSON, nullable=True)
    spend_time = db.Column(db.SmallInteger, nullable=True)
    buy_items = db.Column(db.ARRAY(db.SmallInteger), nullable=True)
    buy_costs = db.Column(db.ARRAY(db.SmallInteger), nullable=True)
    sale_items = db.Column(db.ARRAY(db.SmallInteger), nullable=True)
    sale_costs = db.Column(db.ARRAY(db.SmallInteger), nullable=True)

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
