from base import db


class Inventory(db.Model):
    __tablename__ = "inventory"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer(), primary_key=True)
    head = db.Column(db.SmallInteger(), nullable=True)
    neck = db.Column(db.SmallInteger(), nullable=True)
    earrings = db.Column(db.SmallInteger(), nullable=True)
    hands = db.Column(db.ARRAY(db.SmallInteger()))
    rings = db.Column(db.ARRAY(db.SmallInteger()))
    body = db.Column(db.SmallInteger(), nullable=True)
    legs = db.Column(db.SmallInteger(), nullable=True)
    shoes = db.Column(db.SmallInteger(), nullable=True)
    bag = db.Column(db.ARRAY(db.SmallInteger()))

    def get_all(self):
        "получаем id всех предметов из инвенторя"
        list_ = []
        for key, value in self.to_dict().items():
            if key in ("head", "neck", "earrings", "body", "legs", "shoes"):
                list_.append(value)
            if key in ("hands", "rings", "bag"):
                list_ += value
        return list_
