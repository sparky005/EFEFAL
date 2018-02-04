from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

class SearchClient():

    def __init__(self):
        self.client = Elasticsearch()

    def timestamp_sort(self, hits):
        hits = sorted(hits, key=lambda d : d['@timestamp'])
        return hits
    
    def playbook_index(self):
        s = Search(using=self.client).query("match", type='ansible')
        s = [x.to_dict() for x in s]
        s = self.timestamp_sort(s)
        # TIL that sets don't actually retain order
        list_of_playbooks = set([hit['ansible_playbook'] for hit in s])
        return list_of_playbooks
