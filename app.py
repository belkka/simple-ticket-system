from flask import Flask

import models
from models import db


ticket_system = Flask(__name__)
ticket_system.config.from_prefixed_env('FLASK')
db.init_app(ticket_system)


# TODO: set up a migration tool, Alembic
@ticket_system.cli.command('db_create_all')
def db_create_all():
    """Populate an empty database"""
    with ticket_system.app_context():
        db.create_all()


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
    t = models.Ticket(
        note=f'here is a random number: {x}',
        status=models.Ticket.Status.PENDING,
    )
    db.session.add(t)
    db.session.commit()
    return f'Ok, sure, take this: {t!r}'  # TODO: marshmallow
