import inspect
from flask import Flask
from flask import render_template
from flask import Blueprint
from flask import request
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from efefal.searchclient import SearchClient

bp = Blueprint('efefal', __name__)

# top menubar
nav = Nav()
nav.register_element('top', Navbar(
    View('Home', '.index'),
    View('Playbooks', '.playbook_index'),
    )
)


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.config.update(config or {})
    nav.init_app(app)
    app.register_blueprint(bp)
    Bootstrap(app)
    return app

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/playbooks')
def playbook_index():
    list_of_playbooks = client.playbook_index()
    return render_template('playbooks.html', list_of_playbooks=list_of_playbooks)

@bp.route('/sessions/<playbook>')
def sessions(playbook):
    sessions = client.playbook_sessions(playbook)
    totals = client.playbook_totals(playbook)
    sessions = zip(sessions, totals)
    return render_template('sessions.html', sessions=sessions, playbook=playbook)

@bp.route('/sessions/<playbook>/<session>')
def session_tasks(playbook, session):
    host = request.args.get('host')
    status = request.args.get('status')
    tasks = client.session_tasks(playbook, session, host, status)
    finish = client.session_finish(playbook, session)
    total = client.totals(session)
    hosts = list(finish.keys())
    host_totals = {}
    for host in hosts:
        host_totals[host] = client.totals(session, host)
    return render_template('tasks.html',
                            playbook=playbook,
                            session=session,
                            tasks=tasks,
                            finish=host_totals,
                            total=total)

@bp.route('/devices')
def devices():
    devices = client.get_all_hosts()
    return render_template('devices.html', devices=devices)

app = create_app()
client = SearchClient()
