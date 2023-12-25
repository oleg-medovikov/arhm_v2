from base import db
from datetime import datetime


class Effect(db.Model):
    __tablename__ = "effect"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String)
    # действие
    impact = db.Column(db.JSON)
    # продолжительность действия
    duration = db.Column(db.SmallInteger)
    emoji = db.Column(db.String, nullable=True)
    # увеличивается ли эффект до следующей стадии?
    # словарь всех стадий по-порядку
    stages = db.Column(db.JSON, nullable=True)

    u_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    date_update = db.Column(db.DateTime(), default=datetime.now())

    @property
    def user(self):
        return self._users

    @user.setter
    def user(self, value):
        self._users = value
