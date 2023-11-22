from base import db
from datetime import datetime


class ItemDrop(db.Model):
    __tablename__ = "item_drop"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.SmallInteger, primary_key=True)
    i_id = db.Column(db.SmallInteger, db.ForeignKey("item.id"))
    l_id = db.Column(db.SmallInteger, db.ForeignKey("location.id"))
    p_id = db.Column(db.SmallInteger, db.ForeignKey("person.id"))
    gift = db.Column(db.Boolean)
    active = db.Column(db.Boolean, default=True)
    time_drop = db.Column(db.DateTime, default=datetime.now())
