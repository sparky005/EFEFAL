import inspect
import json
import itertools
from flask import Flask
from flask import render_template
from flask import Blueprint
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
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

"""Helper functions"""
def timestamp_sort(hits):
    hits = sorted(hits, key=lambda d : d['@timestamp'])
    return hits

def calculate_totals(result):
    totals = {
                "ok": 0,
                "failures": 0,
                "unreachable": 0,
                "changed": 0,
                "skipped": 0,
            }
    for host_result in result.keys():
        for key, value in result[host_result].items():
            totals[key] += value
    return totals

def remove_tasklist_duplicates(task_list):
    results = []
    for name, group in itertools.groupby(sorted(task_list,
                                                key=lambda d : d['ansible_task']),
                                                key=lambda d : d['ansible_task']):
        results.append(next(group))
    return results

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
