import flask
import flask_security
from flask_security.models import fsqla_v3 as fsqla

from .database import db
from .auth.models import User, Role


def create_app():
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

    # TODO: set up a migration tool, Alembic
    @ticket_system.cli.command('db_create_all')
    def db_create_all():
        """Populate an empty database"""
        import app.auth.models
        import app.tickets.models

        with ticket_system.app_context():
            db.create_all()
            for i in range(1, 4):
                db.session.add(
                    app.tickets.models.Group(name=f'Customer {i}'),
                )
            db.session.commit()

    import app.tickets.views
    import app.auth.views
    ticket_system.register_blueprint(app.tickets.views.blueprint)
    ticket_system.register_blueprint(app.auth.views.blueprint)

    return ticket_system
