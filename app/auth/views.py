import flask
import sqlalchemy.exc
from flask_security import hash_password

from ..database import db


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

    user = flask.current_app.security.datastore.create_user(
        email=email,
        password=hash_password(password),
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
