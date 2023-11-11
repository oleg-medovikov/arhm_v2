from base import db
from datetime import datetime


class Person(db.Model):
    __tablename__ = "person"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer(), primary_key=True)
    u_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    loc_id = db.Column(db.SmallInteger(), db.ForeignKey("location.id"))
    i_id = db.Column(db.Integer(), db.ForeignKey("inventory.id"))

    gamename = db.Column(db.String(length=50))
    sex = db.Column(db.Boolean)
    profession = db.Column(db.String(length=20))
    create_date = db.Column(db.DateTime(), default=datetime.now())

    gametime = db.Column(db.SmallInteger(), default=1)
    stage = db.Column(db.SmallInteger(), default=1)
    experience = db.Column(db.SmallInteger(), default=0)
    death = db.Column(db.Boolean, default=False)
    death_reason = db.Column(db.String(length=256), nullable=True)
    death_date = db.Column(db.DateTime(), nullable=True)

    money = db.Column(db.SmallInteger())
    proof = db.Column(db.SmallInteger(), default=0)
    bless = db.Column(db.SmallInteger(), default=0)

    health_max = db.Column(db.SmallInteger())
    health = db.Column(db.SmallInteger())
    mind_max = db.Column(db.SmallInteger())
    mind = db.Column(db.SmallInteger())

    speed = db.Column(db.SmallInteger())
    stealth = db.Column(db.SmallInteger())
    strength = db.Column(db.SmallInteger())
    knowledge = db.Column(db.SmallInteger())
    godliness = db.Column(db.SmallInteger())
    luck = db.Column(db.SmallInteger())

    hunger = db.Column(db.SmallInteger(), default=0)
    weary = db.Column(db.SmallInteger(), default=0)

    @property
    def user(self):
        """The user property."""
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def location(self):
        """The location property."""
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def inventory(self):
        """The inventory property."""
        return self._inventory

    @inventory.setter
    def inventory(self, value):
        self._inventory = value
