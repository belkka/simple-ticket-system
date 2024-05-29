import flask
import flask_security
import sqlalchemy.exc
from sqlalchemy.sql.expression import func

from ..database import db
from . import models


blueprint = flask.Blueprint('tickets', __name__, url_prefix='/tickets')


@blueprint.get('/')
def list_tickets():
    tickets = db.session.execute(
        db.select(models.Ticket)
    ).scalars()
    return list(map(repr, tickets))  # TODO: marshmallow


@blueprint.post('/')
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


def get_or_404(query, msg='object does not exist'):
    result = query.fetchone()
    if not result:
        flask.abort(404, msg)
    obj, = result
    return obj


@blueprint.get('/<ticket_id>')
def get_ticket(ticket_id: int):
    ticket = get_or_404(
        db.session.execute(
            db.select(models.Ticket)
            .where(models.Ticket.id == ticket_id)
        ),
    )
    return repr(ticket)


@blueprint.put('/<ticket_id>/status')
@flask_security.auth_required('basic')
def update_status(ticket_id: int):
    ticket = get_or_404(
        db.session.execute(
            db.select(models.Ticket)
            .where(models.Ticket.id == ticket_id)
        ),
    )

    # TODO: figure out how to properly (?) use Flask Principal
    required_role = f'group_analyst:{ticket.group_id}'
    if required_role not in flask_security.current_user.roles:
        flask.abort(403, f'role required: {required_role}')

    try:
        ticket.status = flask.request.json['value']
    except KeyError as err:
        key, = err.args
        flask.abort(400, f'expected json key: {key}')

    db.session.add(ticket)

    try:
        db.session.commit()
    except sqlalchemy.exc.DataError as err:
        details, = err.args
        flask.abort(400, details)

    return repr(ticket)
