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

app = create_app()
client = SearchClient()

@bp.route('/')
def playbook_index():
    list_of_playbooks = client.playbook_index()
    return render_template('playbooks.html', list_of_playbooks=list_of_playbooks)

@bp.route('/runs/<playbook>')
def runs(playbook):
    runs = client.runs(playbook)
    return render_template('runs.html', runs=runs, playbook=playbook)

@bp.route('/runs/tasks/<playbook>/<session>')
def run_tasks(playbook, session):
    tasks, finish, total = client.run_tasks(playbook, session)
    return render_template('tasks.html',
                            playbook=playbook,
                            session=session,
                            tasks=tasks,
                            finish=finish,
                            total=total)
