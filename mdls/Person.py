from base import db
from datetime import datetime


class Person(db.Model):
    __tablename__ = "person"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer(), primary_key=True)
    u_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    loc_id = db.Column(db.SmaInteger(), db.ForeignKey("location.id"))
    i_id = db.Column(db.SmaInteger(), db.ForeignKey("inventory.id"))

    gamename = db.Column(db.String(length=50))
    create_date = db.Column(db.DateTime(), default=datetime.now())
    sex = db.Column(db.Boolean)
    profession = db.Column(db.String(length=20))
    destination = db.Column(db.String(length=256))

    gametime = db.Column(db.SmallInteger())
    stage = db.Column(db.SmallInteger())
    money = db.Column(db.SmallInteger())
    experience = db.Column(db.SmallInteger())
    proof = db.Column(db.SmallInteger())
    bless = db.Column(db.SmallInteger())
    death = db.Column(db.Boolean)
    death_reason = db.Column(db.String(length=256), nullable=True)

    max_health = db.Column(db.SmallInteger())
    health = db.Column(db.SmallInteger())
    max_mind = db.Column(db.SmallInteger())
    mind = db.Column(db.SmallInteger())

    speed = db.Column(db.SmallInteger())
    stealth = db.Column(db.SmallInteger())
    strength = db.Column(db.SmallInteger())
    knowledge = db.Column(db.SmallInteger())
    godliness = db.Column(db.SmallInteger())
    luck = db.Column(db.SmallInteger())

    hunger = db.Column(db.SmallInteger())
    weary = db.Column(db.SmallInteger())