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

@vcr.use_cassette('tests/vcr_cassettes/index.yml', record_mode='new_episodes')
def test_playbook_index(client, playbook_list):
    actual_list = client.playbook_index()
    assert sorted(actual_list) == sorted(playbook_list)

@vcr.use_cassette('tests/vcr_cassettes/test3.yml', record_mode='new_episodes')
def test_sessions(client, session, total_keys):
    sessions = client.playbook_sessions('test3.yml')
    assert isinstance(sessions, list)
    assert len(sessions) == 2
    assert sessions[1]['session'] == session
    assert sessions[0]['@timestamp'] == '2018-02-05T00:51:09.877Z'
    assert sessions[0]['ansible_playbook'] == 'test3.yml'

@vcr.use_cassette('tests/vcr_cassettes/test3.yml', record_mode='new_episodes')
def test_playbook_totals(client, total_keys_upper):
    playbook_totals = client.playbook_totals('test3.yml')
    assert isinstance(playbook_totals, list)
    assert len(playbook_totals) == 2
    assert total_keys_upper == sorted(list(playbook_totals[0].keys()))

@vcr.use_cassette('tests/vcr_cassettes/c8846a16-0c82-11e8-a65f-c48e8ff31cf7/tasks.yml', record_mode='new_episodes')
def test_session_tasks_default(client, session, total_keys):
    tasks = client.session_tasks('test3.yml', session)
    assert isinstance(tasks, list)
    assert len(tasks) > 0
    for task in tasks:
        assert task['ansible_type'] == 'task'
        assert task['session'] == session
        assert task['ansible_host'] in ['localhost', '127.0.0.1']

@vcr.use_cassette('tests/vcr_cassettes/c8846a16-0c82-11e8-a65f-c48e8ff31cf7/tasks_localhost.yml', record_mode='new_episodes')
def test_session_tasks_localhost(client, session, total_keys):
    tasks = client.session_tasks('test3.yml', session, 'localhost')
    assert isinstance(tasks, list)
    assert len(tasks) > 0
    for task in tasks:
        assert task['ansible_type'] == 'task'
        assert task['session'] == session
        assert task['ansible_host'] == 'localhost'
        assert task['status'] in ['FAILED', 'OK']

@vcr.use_cassette('tests/vcr_cassettes/c8846a16-0c82-11e8-a65f-c48e8ff31cf7/tasks_127.0.0.1.yml', record_mode='new_episodes')
def test_session_tasks_127(client, session, total_keys):
    tasks = client.session_tasks('test3.yml', session, '127.0.0.1')
    assert isinstance(tasks, list)
    assert len(tasks) > 0
    for task in tasks:
        assert task['ansible_type'] == 'task'
        assert task['session'] == session
        assert task['ansible_host'] == '127.0.0.1'
        assert task['status'] == 'OK'

@vcr.use_cassette('tests/vcr_cassettes/c8846a16-0c82-11e8-a65f-c48e8ff31cf7/tasks_127.0.0.1_failed.yml', record_mode='new_episodes')
def test_session_tasks_127_failed(client, session, total_keys):
    tasks = client.session_tasks('test3.yml', session, '127.0.0.1', 'FAILED')
    assert isinstance(tasks, list)
    assert len(tasks) == 0, "this should return nothing"

@vcr.use_cassette('tests/vcr_cassettes/c8846a16-0c82-11e8-a65f-c48e8ff31cf7/tasks_127.0.0.1_ok.yml', record_mode='new_episodes')
def test_session_tasks_127_ok(client, session, total_keys):
    tasks = client.session_tasks('test3.yml', session, '127.0.0.1', 'OK')
    assert isinstance(tasks, list)
    assert len(tasks) == 7
    for task in tasks:
        assert task['ansible_type'] == 'task'
        assert task['session'] == session
        assert task['ansible_host'] == '127.0.0.1'
        assert task['status'] == 'OK'

@vcr.use_cassette('tests/vcr_cassettes/c8846a16-0c82-11e8-a65f-c48e8ff31cf7/tasks_localhost_failed.yml', record_mode='new_episodes')
def test_session_tasks_localhost_failed(client, session, total_keys):
    tasks = client.session_tasks('test3.yml', session, 'localhost', 'FAILED')
    assert isinstance(tasks, list)
    assert len(tasks) == 1
    for task in tasks:
        assert task['ansible_type'] == 'task'
        assert task['session'] == session
        assert task['ansible_host'] == 'localhost'
        assert task['status'] == 'FAILED'

@vcr.use_cassette('tests/vcr_cassettes/c8846a16-0c82-11e8-a65f-c48e8ff31cf7/tasks_localhost_ok.yml', record_mode='new_episodes')
def test_session_tasks_localhost_ok(client, session, total_keys):
    tasks = client.session_tasks('test3.yml', session, 'localhost', 'OK')
    assert isinstance(tasks, list)
    assert len(tasks) == 6
    for task in tasks:
        assert task['ansible_type'] == 'task'
        assert task['session'] == session
        assert task['ansible_host'] == 'localhost'
        assert task['status'] == 'OK'

@vcr.use_cassette('tests/vcr_cassettes/c8846a16-0c82-11e8-a65f-c48e8ff31cf7/tasks_all_ok.yml', record_mode='new_episodes')
def test_session_tasks_all_ok(client, session, total_keys):
    tasks = client.session_tasks('test3.yml', session, None, 'OK')
    assert isinstance(tasks, list)
    assert len(tasks) == 7
    for task in tasks:
        assert task['ansible_type'] == 'task'
        assert task['session'] == session
        assert task['ansible_host'] in ['localhost', '127.0.0.1']
        assert task['status'] == 'OK'

@vcr.use_cassette('tests/vcr_cassettes/c8846a16-0c82-11e8-a65f-c48e8ff31cf7/tasks_all_changed.yml', record_mode='new_episodes')
def test_session_tasks_all_ok(client, session, total_keys):
    tasks = client.session_tasks('test3.yml', session, None, 'CHANGED')
    assert isinstance(tasks, list)
    assert len(tasks) == 1
    for task in tasks:
        assert task['ansible_type'] == 'task'
        assert task['session'] == session
        assert task['ansible_host'] in ['localhost', '127.0.0.1']
        assert task['status'] == 'OK'

@vcr.use_cassette('tests/vcr_cassettes/c8846a16-0c82-11e8-a65f-c48e8ff31cf7/tasks_localhost_changed.yml', record_mode='new_episodes')
def test_session_tasks_all_ok(client, session, total_keys):
    tasks = client.session_tasks('test3.yml', session, 'localhost', 'CHANGED')
    assert isinstance(tasks, list)
    assert len(tasks) == 1
    for task in tasks:
        assert task['ansible_type'] == 'task'
        assert task['session'] == session
        assert task['ansible_host'] in ['localhost']
        assert task['status'] == 'OK'

@vcr.use_cassette('tests/vcr_cassettes/c8846a16-0c82-11e8-a65f-c48e8ff31cf7/tasks_127_changed.yml', record_mode='new_episodes')
def test_session_tasks_all_ok(client, session, total_keys):
    tasks = client.session_tasks('test3.yml', session, '127.0.0.1', 'CHANGED')
    assert isinstance(tasks, list)
    assert len(tasks) == 1
    for task in tasks:
        assert task['ansible_type'] == 'task'
        assert task['session'] == session
        assert task['ansible_host'] in ['127.0.0.1']
        assert task['status'] == 'OK'

@vcr.use_cassette('tests/vcr_cassettes/c8846a16-0c82-11e8-a65f-c48e8ff31cf7/tasks_all_failed.yml', record_mode='new_episodes')
def test_session_tasks_all_failed(client, session, total_keys):
    tasks = client.session_tasks('test3.yml', session, None, 'FAILED')
    assert isinstance(tasks, list)
    assert len(tasks) == 1
    for task in tasks:
        assert task['ansible_type'] == 'task'
        assert task['session'] == session
        assert task['ansible_host'] in ['localhost', '127.0.0.1']
        assert task['status'] == 'FAILED'

@vcr.use_cassette('tests/vcr_cassettes/c8846a16-0c82-11e8-a65f-c48e8ff31cf7/finish.yml', record_mode='new_episodes')
def test_session_finish(client, session):
    finish = client.session_finish('test3.yml', session)
    assert isinstance(finish, dict)
    assert sorted(['localhost', '127.0.0.1']) == sorted(list(finish.keys()))

@vcr.use_cassette('tests/vcr_cassettes/c8846a16-0c82-11e8-a65f-c48e8ff31cf7/totals.yml', record_mode='new_episodes')
def test_totals(client, session, total_keys):
    totals = client.totals(session)
    assert isinstance(totals, dict)
    assert totals['OK'] == 11
    assert totals['CHANGED'] == 2
    assert totals['FAILED'] == 1

@vcr.use_cassette('tests/vcr_cassettes/c8846a16-0c82-11e8-a65f-c48e8ff31cf7/hosts.yml', record_mode='new_episodes')
def test_get_hosts(client, session):
    hosts = client.get_hosts(session)
    assert isinstance(hosts, list)
    assert sorted(['localhost', '127.0.0.1']) == sorted(hosts)

@vcr.use_cassette('tests/vcr_cassettes/c8846a16-0c82-11e8-a65f-c48e8ff31cf7/totals_localhost.yml', record_mode='new_episodes')
def test_totals_one_host(client, session):
    totals = client.totals(session, 'localhost')
    assert isinstance(totals, dict)
    assert totals['OK'] == 5
    assert totals['CHANGED'] == 1
    assert totals['FAILED'] == 1

@vcr.use_cassette('tests/vcr_cassettes/c8846a16-0c82-11e8-a65f-c48e8ff31cf7/totals_127.yml', record_mode='new_episodes')
def test_totals_one_host(client, session):
    totals = client.totals(session, '127.0.0.1')
    assert isinstance(totals, dict)
    assert totals['OK'] == 6
    assert totals['CHANGED'] == 1
    assert totals['FAILED'] == 0
