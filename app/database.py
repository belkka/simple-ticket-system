import sqlalchemy.orm
from flask_sqlalchemy import SQLAlchemy


class Base(sqlalchemy.orm.DeclarativeBase):
    def __repr__(self):
        self.id  # hack
        ret = dict(self.__dict__)
        del ret['_sa_instance_state']
        return repr(ret)


db = SQLAlchemy(model_class=Base)

