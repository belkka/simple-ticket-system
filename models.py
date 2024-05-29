import enum

import sqlalchemy.orm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    def __repr__(self):
        self.id  # hack
        ret = dict(self.__dict__)
        del ret['_sa_instance_state']
        return repr(ret)


db = SQLAlchemy(model_class=Base)


class Group(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Ticket(db.Model):
    class Status(enum.StrEnum):
        PENDING = 'pending'
        IN_REVIEW = 'in_review'
        CLOSED = 'closed'

        # TODO: remove when proper serialization is implemented
        def __repr__(self):
            return repr(self.value)

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[Status]
    note: Mapped[str]

    group_id: Mapped[int] = mapped_column(ForeignKey(Group.id))
    group: Mapped[Group] = sqlalchemy.orm.relationship()
