import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database"""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = get_db()
    with app.open_resource('schema_sql', mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()


@app.cli.command('init_db')
def initdb_command():
    """Initializes the database"""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite3.db'):
        g.sqlite3_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes db at the end of the request"""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
