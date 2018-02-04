import inspect
import json
import itertools
from flask import Flask
from flask import render_template
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

app = Flask(__name__)

@app.route('/')
def playbook_index():
    client = Elasticsearch()
    s = Search(using=client).query("match", type='ansible')
    list_of_playbooks = set([hit.ansible_playbook for hit in s.scan()])
    # can't return a whole list
    # also, right now this returns the same playbook name many times
    return render_template('playbooks.html', list_of_playbooks=list_of_playbooks)

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


@app.route('/runs/<playbook>')
def runs(playbook):
    client = Elasticsearch()
    s = Search(using=client).query("match_phrase", ansible_playbook=playbook).filter("term", ansible_type="finish")
    # we have to calculate the totals for all the runs
    # as totals are tallied per host
    totals = [calculate_totals(json.loads(x.ansible_result)) for x in s]
    runs = zip(s.scan(),totals)
    return render_template('runs.html', runs=runs, playbook=playbook)

@app.route('/runs/tasks/<playbook>/<session>')
def run_tasks(playbook, session):
    # TODO we dont actually need the session passed to the template
    # we just need it to construct the URL
    # what we actually need to pass to the template is the task list
    client = Elasticsearch()
    s = Search(using=client).query("match_phrase", session=session) \
                            .filter("term", ansible_type="task")
    finish = Search(using=client).query("match_phrase", session=session) \
                            .filter("term", ansible_type="finish")
    tasks = s.scan()
    tasks = [task.to_dict() for task in tasks]
    tasks = remove_tasklist_duplicates(tasks)
    finish = finish.scan()
    finish = [x.to_dict() for x in finish]
    finish = json.loads(finish[0]['ansible_result'])
    total = calculate_totals(finish)
    return render_template('tasks.html',
                            playbook=playbook,
                            session=session,
                            tasks=tasks,
                            finish=finish,
                            total=total)
