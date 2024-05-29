import flask
from flask_security import auth_required


blueprint = flask.Blueprint('auth', __name__)


@blueprint.get("/me")
@auth_required('basic')
def say_hello():
    return flask.render_template_string(
        "Hello {{ current_user.email }}"
    )


