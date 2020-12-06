import click
from flask import current_app
from flask.cli import with_appcontext

from .. import db

def init_db():
    with current_app.app_context():
        from .models import Department, Employee
        db.create_all()


def drop_db():
    with current_app.app_context():
        db.session.remove()
        db.drop_all()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

@click.command('drop-db')
@with_appcontext
def drop_db_command():
    drop_db()
    click.echo('Dropped the database.')


def register_db_commands(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(drop_db_command)
