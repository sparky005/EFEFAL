import json
import pytest
import vcr

def test_timestamp_sort(client, dummy_hits):
    sorted_hits = client.timestamp_sort(dummy_hits)
    assert isinstance(sorted_hits, list)
    assert sorted_hits != dummy_hits, "Sorted list is probably different than unsorted list"
    assert len(sorted_hits) == len(dummy_hits), "Sorted list should have the same length"
    assert len(sorted_hits) == 14, "Length of sorted hits should be 14"

def test_remove_tasklist_duplicates(client, dummy_hits):
    deduped_hits = client.remove_tasklist_duplicates(dummy_hits)
    assert isinstance(deduped_hits, list), "taskslist removal should return list"
    assert deduped_hits != dummy_hits, "Tasklist removal should alter list"
    assert len(deduped_hits) <= len(dummy_hits), "Deduped list should be <= original"
    assert len(deduped_hits) == 7, "Here, list should be half the size of original"

def test_calculate_totals(client, dummy_hits, dummy_finish, total_keys):
    dummy_totals = client.calculate_totals(json.loads(dummy_finish[0]['ansible_result']))
    assert isinstance(dummy_totals, dict), "calculate_totals should return dict"
    assert total_keys == sorted(list(dummy_totals.keys()))
    for key, value in dummy_totals.items():
        assert isinstance(value, int), "Should have integer totals"

@vcr.use_cassette('tests/vcr_cassettes/index.yml')
def test_playbook_index(client, playbook_list):
    actual_list = client.playbook_index()
    assert sorted(actual_list) == sorted(playbook_list)

@vcr.use_cassette('tests/vcr_cassettes/test3.yml')
def test_runs(client, session, total_keys):
    actual_runs = client.runs('test3.yml')
    runs, totals = zip(*actual_runs)
    assert isinstance(runs, tuple)
    assert len(runs) == 1
    assert runs[0]['session'] == session
    assert runs[0]['@timestamp'] == '2018-02-03T22:21:06.617Z'
    assert runs[0]['ansible_playbook'] == 'test3.yml'
    assert isinstance(totals, tuple)
    assert len(totals) == 1
    assert len(runs) == len(totals), "Totals and runs should be same length"
    assert total_keys == sorted(list(totals[0].keys()))

@vcr.use_cassette('tests/vcr_cassettes/8262ba60-0930-11e8-8eaf-c48e8ff31cf7.yml')
def test_run_tasks(client, session, total_keys):
    tasks, finish, total = client.run_tasks('test3.yml', session)
    assert isinstance(tasks, list)
    for task in tasks:
        assert task['ansible_type'] == 'task'
        assert task['session'] == session
    assert isinstance(finish, dict)
    assert sorted(['localhost', '127.0.0.1']) == sorted(list(finish.keys()))
    assert isinstance(total, dict)
    assert total_keys == sorted(list(total.keys()))
