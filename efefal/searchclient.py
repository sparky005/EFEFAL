import json
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

class SearchClient():

    def __init__(self):
        self.client = Elasticsearch()

    def timestamp_sort(self, hits):
        hits = sorted(hits, key=lambda d : d['@timestamp'])
        return hits
    
    def calculate_totals(self, result):
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

    def playbook_index(self):
        s = Search(using=self.client).query("match", type='ansible')
        s = [x.to_dict() for x in s]
        s = self.timestamp_sort(s)
        # TIL that sets don't actually retain order
        list_of_playbooks = set([hit['ansible_playbook'] for hit in s])
        return list_of_playbooks

    def runs(self, playbook):
        s = Search(using=self.client).query("match_phrase", ansible_playbook=playbook).filter("term", ansible_type="finish")
        # we have to calculate the totals for all the runs
        # as totals are tallied per host
        s = [hit.to_dict() for hit in s]
        s = self.timestamp_sort(s)
        totals = [self.calculate_totals(json.loads(x['ansible_result'])) for x in s]
        runs = zip(s,totals)
        return runs
