import app.tickets.views
from app import ticket_system, db


# TODO: set up a migration tool, Alembic
@ticket_system.cli.command('db_create_all')
def db_create_all():
    """Populate an empty database"""
    from app.tickets.models import Group

    with ticket_system.app_context():
        db.create_all()
        for i in range(1, 4):
            db.session.add(Group(name=f'Customer {i}'))
        db.session.commit()


ticket_system.register_blueprint(app.tickets.views.blueprint)
