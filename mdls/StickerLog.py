from base import db


class StickerLog(db.Model):
    __tablename__ = "sticker_log"
    __table_args__ = {"extend_existing": True}

    chat_id = db.Column(db.BigInteger(), primary_key=True)
    message_id = db.Column(db.BigInteger())
