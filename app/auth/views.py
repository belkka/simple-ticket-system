import flask
import sqlalchemy.exc
from flask_security import hash_password

from ..database import db
from . import models


blueprint = flask.Blueprint('auth', __name__)


@blueprint.post('/me')
def register():
    data = flask.request.form or flask.request.json
    try:
        email = data['email']
        password = data['password']
    except KeyError as err:
        key, = err.args
        flask.abort(400, f"Missing key: {key}")

    # manager of group #1 and analyst of group#2
    # pretty standard role combination, so it's default for new users
    default_roles = 'group_manager:1,group_analyst:2'

    roles = data.get('roles', default_roles).split(',')
    for role in roles:
        flask.current_app.security.datastore.find_or_create_role(
            name=role,
        )

    user = flask.current_app.security.datastore.create_user(
        email=email,
        password=hash_password(password),
        roles=roles,
    )
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as err:
        details, = err.args
        return f"Apparently, account exists. {details}", 409
    else:
        return f"Welcome to the club, number {user.id}", 201


@blueprint.get('/me')
def say_hello():
    return flask.render_template_string("""
        Hello, stranger.
        <form method="post">
            <label for="email">e-mail</label>
            <input type="text" name="email" placeholder="email"></input>

            <label for="password">password</label>
            <input type="password" name="password"></input>

            <button type="submit">Register</button>
        </form>
    """)
