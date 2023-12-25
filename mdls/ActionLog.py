from base import db
from datetime import datetime


class ActionLog(db.Model):
    __tablename__ = "action_log"
    __table_args__ = {"extend_existing": True}

    time = db.Column(db.DateTime, default=datetime.now(), primary_key=True)
    p_id = db.Column(db.SmallInteger, db.ForeignKey("person.id"))
    gametime = db.Column(db.SmallInteger)
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

    @property
    def person(self):
        """The person property."""
        return self._person

    @person.setter
    def person(self, value):
        self._person = value

    @property
    def action(self):
        """The action property."""
        return self._action

    @action.setter
    def action(self, value):
        self._action = value

    @property
    def event(self):
        """The event property."""
        return self._event

    @event.setter
    def event(self, value):
        self._event = value

    @property
    def location(self):
        """The location property."""
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def monster(self):
        """The monster property."""
        return self._monster

    @monster.setter
    def monster(self, value):
        self._monster = value
