import flask
from  sqlalchemy.sql.expression import func

import models
from models import db


ticket_system = flask.Flask(__name__)
ticket_system.config.from_prefixed_env('FLASK')
db.init_app(ticket_system)


# TODO: set up a migration tool, Alembic
@ticket_system.cli.command('db_create_all')
def db_create_all():
    """Populate an empty database"""
    with ticket_system.app_context():
        db.create_all()
        for i in range(1, 4):
            db.session.add(models.Group(name=f'Customer {i}'))
        db.session.commit()


@ticket_system.get('/tickets')
def list_tickets():
    tickets = db.session.execute(
        db.select(models.Ticket)
    ).scalars()
    return list(map(repr, tickets))  # TODO: marshmallow


@ticket_system.post('/tickets')
def create_random_ticket():
    import random
    x = random.randint(1, 10000)
    random_group_id, = db.session.execute(
        db.select(models.Group.id)
        .order_by(func.random())
        .limit(1)
    ).first()
    t = models.Ticket(
        note=f'here is a random number: {x}',
        status=models.Ticket.Status.PENDING,
        group_id=random_group_id,
    )
    db.session.add(t)
    db.session.commit()
    return flask.Response(
        f'Ok, sure, take this: {t!r}',  # TODO: marshmallow
        content_type='text/plain',
    )
