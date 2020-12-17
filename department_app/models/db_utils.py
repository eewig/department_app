import click
from flask import current_app
from flask.cli import with_appcontext

from .. import db


def init_db():
    """Create all models in database."""
    with current_app.app_context():
        from .models import Department, Employee
        db.create_all()


def drop_db():
    """Delete all models in database."""
    with current_app.app_context():
        db.session.remove()
        db.drop_all()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Create all models and print the appropriate message."""
    init_db()
    click.echo('Initialized the database.')


@click.command('drop-db')
@with_appcontext
def drop_db_command():
    """Delete all models and print the appropriate message."""
    drop_db()
    click.echo('Dropped the database.')


def register_db_commands(app):
    """Registers create and delete models' commands."""
    app.cli.add_command(init_db_command)
    app.cli.add_command(drop_db_command)
