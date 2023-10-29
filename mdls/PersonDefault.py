from base import db
from datetime import datetime


class PersonDefault(db.Model):
    "таблица с разбросами параметров у разных профессий"
    __tablename__ = "person_default"
    __table_args__ = {"extend_existing": True}

    profession = db.Column(db.String(length=20), primary_key=True)
    start_loc_id = db.Column(db.SmallInteger(), db.ForeignKey("location.id"))
    start_items = db.Column(db.ARRAY(db.SmallInteger()))
    money_min = db.Column(db.SmallInteger())
    money_max = db.Column(db.SmallInteger())
    healf_min = db.Column(db.SmallInteger())
    healf_max = db.Column(db.SmallInteger())
    mind_min = db.Column(db.SmallInteger())
    mind_max = db.Column(db.SmallInteger())
    speed_min = db.Column(db.SmallInteger())
    speed_max = db.Column(db.SmallInteger())
    stealth_min = db.Column(db.SmallInteger())
    stealth_max = db.Column(db.SmallInteger())
    strength_min = db.Column(db.SmallInteger())
    strength_max = db.Column(db.SmallInteger())
    knowledge_min = db.Column(db.SmallInteger())
    knowledge_max = db.Column(db.SmallInteger())
    godliness_min = db.Column(db.SmallInteger())
    godliness_max = db.Column(db.SmallInteger())
    luck_min = db.Column(db.SmallInteger())
    luck_max = db.Column(db.SmallInteger())

    u_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    update = db.Column(db.DateTime(), default=datetime.now())

    @property
    def user(self):
        return self._users

    @user.setter
    def user(self, value):
        self._users = value
