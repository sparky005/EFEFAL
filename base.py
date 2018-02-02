import inspect
import json
from flask import Flask
from flask import render_template
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

app = Flask(__name__)

@app.route('/')
def playbook_index():
    client = Elasticsearch()
    # TODO: why did this suddenly stop returning all playbooks
    s = Search(using=client, index=("%{[@metadata][beat]}-*")).query("match", type='ansible')
    list_of_playbooks = set([hit.ansible_playbook for hit in s.execute()])
    # can't return a whole list
    # also, right now this returns the same playbook name many times
    return render_template('playbooks.html', list_of_playbooks=list_of_playbooks)

def calculate_totals(result):
    result = json.loads(result)
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

@app.route('/runs/<playbook>')
def runs(playbook):
    client = Elasticsearch()
    s = Search(using=client, index=("%{[@metadata][beat]}-*")).query("match", ansible_playbook=playbook).filter("term", ansible_type="finish")
    # we have to calculate the totals for all the runs
    # as totals are tallied per host
    totals = [calculate_totals(x.ansible_result) for x in s]
    runs = zip(s.execute(),totals)
    return render_template('runs.html', runs=runs, playbook=playbook)
