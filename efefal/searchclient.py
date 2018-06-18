import json
import itertools
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

class SearchClient():

    def __init__(self):
        self.client = Elasticsearch()

    def timestamp_to_dt(self, timestamp):
        """
        converts weird timestamps into workable dt objects
        """
        # drop milliseconds
        ix = timestamp.find('.')
        d = datetime.strptime(timestamp[:ix], '%Y-%m-%dT%H:%M:%S')
        return d

    def timestamp_sort(self, hits):
        hits = sorted(hits, key=lambda d : d['@timestamp'])
        return hits

    def reverse_timestamp_sort(self, hits):
        hits = sorted(hits, key=lambda d : d['@timestamp'], reverse=True)
        return hits

    def calculate_totals(self, result):
        """Takes a 'finish' as a param and provides totals"""
        totals = {
                    "ok": 0,
                    "failed": 0,
                    "unreachable": 0,
                    "changed": 0,
                    "skipped": 0,
                }
        for host_result in result.keys():
            for key, value in result[host_result].items():
                if key == 'failures':
                    totals['failed'] += value
                else:
                    totals[key] += value
        return totals

    def remove_tasklist_duplicates(self, task_list):
        # this has the side-effect of removing same-named tasks
        # oh well
        results = []
        for name, group in itertools.groupby(sorted(task_list,
                                                    key=lambda d : d['ansible_task']),
                                                    key=lambda d : d['ansible_task']):
            results.append(next(group))
        return results

    def playbook_index(self):
        s = Search(using=self.client).query("match", type='ansible')
        s = [x.to_dict() for x in s]
        s = self.reverse_timestamp_sort(s)
        # TIL that sets don't actually retain order
        list_of_playbooks = set([hit['ansible_playbook'] for hit in s])
        return list_of_playbooks

    def playbook_totals(self, playbook):
        """gets totals for each run of a single playbook using a 'finish' object"""
        s = Search(using=self.client).query("match_phrase", ansible_playbook=playbook).filter("term", ansible_type="finish")
        s = [hit.to_dict() for hit in s]
        sessions = [hit['session'] for hit in s]
        totals = [self.totals(session) for session in sessions]
        return totals

    def playbook_sessions(self, playbook):
        """get list of all sessions for a single playook"""
        s = Search(using=self.client).query("match_phrase", ansible_playbook=playbook).filter("term", ansible_type="finish")
        s = [hit.to_dict() for hit in s]
        for hit in s:
            hit['@timestamp'] = self.timestamp_to_dt(hit['@timestamp'])
        s = self.reverse_timestamp_sort(s)
        return s

    def session_tasks(self, playbook, session, host=None, status=None):
        """Get info for a single run (session) of a single playbook"""
        # handle the special case (changed) first
        if host and status == 'CHANGED':
            s = Search(using=self.client).query("match_phrase", session=session) \
                                    .filter("term", ansible_type="task") \
                                    .filter("match", status='OK') \
                                    .filter("term", ansible_host=host) \
                                    .filter("match_phrase", ansible_result="changed: true")
        elif status == 'CHANGED':
            s = Search(using=self.client).query("match_phrase", session=session) \
                                    .filter("term", ansible_type="task") \
                                    .filter("match", status='OK') \
                                    .filter("match_phrase", ansible_result="changed: true")
        elif host and status:
            s = Search(using=self.client).query("match_phrase", session=session) \
                                    .filter("term", ansible_type="task") \
                                    .filter("term", ansible_host=host) \
                                    .filter("match", status=status)
        elif host:
            s = Search(using=self.client).query("match_phrase", session=session) \
                                    .filter("term", ansible_type="task") \
                                    .filter("term", ansible_host=host)
        elif status:
            s = Search(using=self.client).query("match_phrase", session=session) \
                                    .filter("term", ansible_type="task") \
                                    .filter("match", status=status)
        else:
            s = Search(using=self.client).query("match_phrase", session=session) \
                                    .filter("term", ansible_type="task")
        tasks = s.scan()
        tasks = [task.to_dict() for task in tasks]
        # make sure we don't remove duplicates
        # when we actually care about all the tasks
        if not status:
            tasks = self.remove_tasklist_duplicates(tasks)
        tasks = self.timestamp_sort(tasks)
        for task in tasks:
            # remove word TASK: from the beginning of each task
            space = task['ansible_task'].find(' ')
            task['ansible_task'] = task['ansible_task'][space:]
            task['@timestamp'] = self.timestamp_to_dt(task['@timestamp'])
        return tasks

    def session_finish(self, playbook, session):
        """Get finish information for a single playbook run"""
        finish = Search(using=self.client).query("match_phrase", session=session) \
                                .filter("term", ansible_type="finish")
        finish = finish.scan()
        finish = [x.to_dict() for x in finish]
        finish = json.loads(finish[0]['ansible_result'])
        for host in finish:
            finish[host]['failed'] = finish[host].pop('failures')

        # some hackery to reorder the dict
        for key in ["ok", "failed", "unreachable", "changed", "skipped"]:
            for host in finish:
                finish[host][key] = finish[host].pop(key)
        return finish

    def get_all_hosts(self, timeframe=7):
        """
        Get all hosts in database
        timeframe = timeframe to search in days
        """
        s = Search(using=self.client) \
            .query("range", ** {'@timestamp': {'lt': 'now', 'gt': 'now-{}d'.format(timeframe)}}) \
            .query("match", type='ansible')
        s = [hit.to_dict() for hit in s]
        hosts = [hit['ansible_host'] for hit in s]
        return set(hosts)

    def get_hosts(self, session):
        """Get the hosts that were in a given session"""
        s = Search(using=self.client).query("match_phrase", session=session) \
                                    .filter("term", ansible_type="finish")
        finishes = s.scan()
        finishes = [x.to_dict() for x in finishes]
        return list(json.loads(finishes[0]['ansible_result']).keys())

    def totals(self, session, host=None):
        """
        Calculates and returns the totals for a given session
        if host is given, only get totals for the single host
        else, the entire session
        """
        if host:
            s = Search(using=self.client).query("match_phrase", session=session) \
                                    .filter("term", ansible_type="task") \
                                    .filter("term", ansible_host=host)
        else:
            s = Search(using=self.client).query("match_phrase", session=session) \
                                        .filter("term", ansible_type="task")
        tasks = s.scan()
        tasks = [task.to_dict() for task in tasks]
        totals = {
                    "OK": 0,
                    "FAILED": 0,
                    "UNREACHABLE": 0,
                    "CHANGED": 0,
                    "SKIPPED": 0,
                }
        for task in tasks:
            result = task['status']
            if result == 'OK':
                # check if it was a change
                if json.loads(task['ansible_result'])['changed'] == True:
                    result = 'CHANGED'
            totals[result] += 1
        return totals

