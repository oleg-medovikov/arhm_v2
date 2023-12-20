from base import db
from datetime import datetime


class ActionLog(db.Model):
    __tablename__ = "action_log"
    __table_args__ = {"extend_existing": True}

    time = db.Column(db.DateTime, default=datetime.now(), primary_key=True)
    p_id = db.Column(db.SmallInteger, db.ForeignKey("person.id"))
    gametime = db.Column(db.SmallInt)
    a_id = db.Column(db.SmallInteger, db.ForeignKey("action.id"))
    # закончено ли действие
    finish = db.Column(db.Boolean)
    # если это ивент
    e_id = db.Column(db.SmallInteger, db.ForeignKey("event.id"), nullable=True)
    # если был выбор, то какой
    choice = db.Column(db.Boolean, nullable=True)
    # если была проверка, то результат
    check = db.Column(db.Boolean, nullable=True)
    # если диалог
    d_id = db.Column(db.SmallInteger, nullable=True)
    # если произошло перемещение, то куда.
    loc_start = db.Column(db.SmallInteger, db.ForeignKey("location.id"), nullable=True)
    loc_finish = db.Column(db.SmallInteger, db.ForeignKey("location.id"), nullable=True)
    # если было сражение с монстром
    m_id = db.Column(db.SmallInteger, db.ForeignKey("monster.id"))
    victory = db.Column(db.Boolean)
