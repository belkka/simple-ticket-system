from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    def __repr__(self):
        self.id  # hack
        ret = dict(self.__dict__)
        del ret['_sa_instance_state']
        return repr(ret)


db = SQLAlchemy(model_class=Base)


class Ticket(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    note: Mapped[str]
