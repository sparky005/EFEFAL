import inspect
from flask import Flask
from flask import render_template
from flask import Blueprint
from flask import request
from efefal.searchclient import SearchClient

bp = Blueprint('efefal', __name__)


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.config.update(config or {})
    app.register_blueprint(bp)
    return app

@bp.route('/')
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
    return render_template('tasks.html',
                            playbook=playbook,
                            session=session,
                            tasks=tasks,
                            finish=finish,
                            total=total)
app = create_app()
client = SearchClient()

