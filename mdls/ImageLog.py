from base import db


class ImageLog(db.Model):
    __tablename__ = "image_log"
    __table_args__ = {"extend_existing": True}

    chat_id = db.Column(db.BigInteger(), primary_key=True)
    message_id = db.Column(db.BigInteger())
    name = db.Column(db.String(), nullable=True)
