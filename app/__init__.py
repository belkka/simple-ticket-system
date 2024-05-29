import flask
import sqlalchemy.orm
from flask_sqlalchemy import SQLAlchemy


ticket_system = flask.Flask(__name__)
ticket_system.config.from_prefixed_env('FLASK')


class Base(sqlalchemy.orm.DeclarativeBase):
    def __repr__(self):
        self.id  # hack
        ret = dict(self.__dict__)
        del ret['_sa_instance_state']
        return repr(ret)


db = SQLAlchemy(model_class=Base)
db.init_app(ticket_system)
