import flask
import flask_security
from flask_security.models import fsqla_v3 as fsqla

from .database import db
from .auth.models import User, Role


ticket_system = flask.Flask(__name__)
ticket_system.config.from_prefixed_env('FLASK')

if ticket_system.debug:
    from pprint import pprint as print
    print(dict(ticket_system.config))

db.init_app(ticket_system)

ticket_system.security = flask_security.Security(
    ticket_system,
    flask_security.SQLAlchemyUserDatastore(db, User, Role),
)

