from base import db


class Inventory(db.Model):
    __tablename__ = "inventory"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer(), primary_key=True)
    head = db.Column(db.SmallInteger(), nullable=True)
    earrings = db.Column(db.SmallInteger(), nullable=True)
    hands = db.Column(db.ARRAY(db.SmallInteger()), nullable=True)
    rings = db.Column(db.ARRAY(db.SmallInteger()), nullable=True)
    body = db.Column(db.SmallInteger(), nullable=True)
    legs = db.Column(db.SmallInteger(), nullable=True)
    shoes = db.Column(db.SmallInteger(), nullable=True)
    bag = db.Column(db.ARRAY(db.SmallInteger()), nullable=True)
