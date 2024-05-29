import flask
from sqlalchemy.sql.expression import func

from ..database import db
from . import models


blueprint = flask.Blueprint('tickets', __name__, url_prefix='/')


@blueprint.get('/tickets')
def list_tickets():
    tickets = db.session.execute(
        db.select(models.Ticket)
    ).scalars()
    return list(map(repr, tickets))  # TODO: marshmallow


@blueprint.post('/tickets')
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
