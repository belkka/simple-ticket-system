import enum

import sqlalchemy.orm
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..database import db


class Group(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)


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
