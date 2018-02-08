import inspect
from flask import Flask
from flask import render_template
from flask import Blueprint
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
def runs(playbook):
    runs = client.playbook_runs(playbook)
    totals = client.playbook_totals(playbook)
    runs = zip(runs, totals)
    return render_template('runs.html', runs=runs, playbook=playbook)

@bp.route('/sessions/<playbook>/<session>')
def session_tasks(playbook, session):
    tasks = client.session_tasks(playbook, session)
    finish = client.session_finish(playbook, session)
    total = client.calculate_totals(finish)
    return render_template('tasks.html',
                            playbook=playbook,
                            session=session,
                            tasks=tasks,
                            finish=finish,
                            total=total)
app = create_app()
client = SearchClient()

