import vcr

@vcr.use_cassette('tests/vcr_cassettes/pages/index.yml', record_mode='new_episodes')
def test_index(app):
    rv = app.get('/')
    assert b'By Playbook' in rv.data
    assert b'By Device' in rv.data
    assert b'By Session' in rv.data

@vcr.use_cassette('tests/vcr_cassettes/pages/playbook_index.yml', record_mode='new_episodes')
def test_playbook_index(app):
    rv = app.get('/playbooks')
    assert b'test.yml' in rv.data
    assert b'test2.yml' in rv.data
    assert b'test3.yml' in rv.data
    assert b'<a href="/sessions/test2.yml"> test2.yml' in rv.data

@vcr.use_cassette('tests/vcr_cassettes/pages/test3.yml', record_mode='new_episodes')
def test_sessions(app):
    rv = app.get('/sessions/test3.yml')
    assert b'SessionID' in rv.data
    assert b'Timestamp' in rv.data
    assert b'Playbook' in rv.data
    assert b'Ok' in rv.data
    assert b'Failed' in rv.data
    assert b'Unreachable' in rv.data
    assert b'Changed' in rv.data
    assert b'Skipped' in rv.data
    assert b'a5cba87a-0a0e-11e8-b454-c48e8ff31cf7' in rv.data
    assert b'test3.yml' in rv.data
    assert b'<a href="/sessions/test3.yml/a5cba87a-0a0e-11e8-b454-c48e8ff31cf7">a5cba87a-0a0e-11e8-b454-c48e8ff31cf7</a>' in rv.data

@vcr.use_cassette('tests/vcr_cassettes/pages/c8846a16-0c82-11e8-a65f-c48e8ff31cf7.yml', record_mode='new_episodes')
def test_session_tasks_all(app):
    rv = app.get('sessions/test3.yml/c8846a16-0c82-11e8-a65f-c48e8ff31cf7')
    hosts = [b'127.0.0.1', b'localhost']
    tasks = [
                b'Gathering Facts',
                b'say hi',
                b'say hi 2',
                b'say hi 3',
                b'say hi 4',
                b'fail',
                b'change something'
            ]
    assert b'Host' in rv.data
    assert b'Ok' in rv.data
    assert b'Failures' in rv.data
    assert b'Unreachable' in rv.data
    assert b'Changed' in rv.data
    assert b'Skipped' in rv.data
    assert b'Timestamp' in rv.data
    assert b'c8846a16-0c82-11e8-a65f-c48e8ff31cf7' in rv.data
    for host in hosts:
        assert host in rv.data
    for task in tasks:
        assert task in rv.data

@vcr.use_cassette('tests/vcr_cassettes/pages/c8846a16-0c82-11e8-a65f-c48e8ff31cf7_localhost.yml', record_mode='new_episodes')
def test_session_tasks_localhost(app):
    rv = app.get('sessions/test3.yml/c8846a16-0c82-11e8-a65f-c48e8ff31cf7?host=localhost')
    hosts = [b'localhost']
    tasks = [
                b'Gathering Facts',
                b'say hi',
                b'say hi 2',
                b'say hi 3',
                b'say hi 4',
                b'fail',
                b'change something'
            ]
    assert b'Host' in rv.data
    assert b'Ok' in rv.data
    assert b'Failures' in rv.data
    assert b'Unreachable' in rv.data
    assert b'Changed' in rv.data
    assert b'Skipped' in rv.data
    assert b'Timestamp' in rv.data
    assert b'c8846a16-0c82-11e8-a65f-c48e8ff31cf7' in rv.data
    for host in hosts:
        assert host in rv.data
    for task in tasks:
        assert task in rv.data
    assert b'FAILED' in rv.data
    assert b'OK' in rv.data

@vcr.use_cassette('tests/vcr_cassettes/pages/c8846a16-0c82-11e8-a65f-c48e8ff31cf7_127.0.0.1.yml', record_mode='new_episodes')
def test_session_tasks_127(app):
    rv = app.get('sessions/test3.yml/c8846a16-0c82-11e8-a65f-c48e8ff31cf7?host=127.0.0.1')
    hosts = [b'127.0.0.1']
    tasks = [
                b'Gathering Facts',
                b'say hi',
                b'say hi 2',
                b'say hi 3',
                b'say hi 4',
                b'fail',
                b'change something'
            ]
    assert b'Host' in rv.data
    assert b'Ok' in rv.data
    assert b'Failures' in rv.data
    assert b'Unreachable' in rv.data
    assert b'Changed' in rv.data
    assert b'Skipped' in rv.data
    assert b'Timestamp' in rv.data
    assert b'c8846a16-0c82-11e8-a65f-c48e8ff31cf7' in rv.data
    for host in hosts:
        assert host in rv.data
    for task in tasks:
        assert task in rv.data
    assert b'OK' in rv.data

@vcr.use_cassette('tests/vcr_cassettes/pages/c8846a16-0c82-11e8-a65f-c48e8ff31cf7_127.0.0.1_failed.yml', record_mode='new_episodes')
def test_session_tasks_127_failed(app):
    rv = app.get('sessions/test3.yml/c8846a16-0c82-11e8-a65f-c48e8ff31cf7?host=127.0.0.1&status=FAILED')
    hosts = [b'127.0.0.1']
    tasks = [
                b'Gathering Facts',
                b'say hi',
                b'say hi 2',
                b'say hi 3',
                b'say hi 4',
                b'fail',
                b'change something'
            ]
    assert b'Host' in rv.data
    assert b'Ok' in rv.data
    assert b'Failures' in rv.data
    assert b'Unreachable' in rv.data
    assert b'Changed' in rv.data
    assert b'Skipped' in rv.data
    assert b'Timestamp' in rv.data
    assert b'c8846a16-0c82-11e8-a65f-c48e8ff31cf7' in rv.data
    for host in hosts:
        assert host in rv.data
    for task in tasks:
        assert task not in rv.data, "No failed tasks should appear for 127"

@vcr.use_cassette('tests/vcr_cassettes/pages/c8846a16-0c82-11e8-a65f-c48e8ff31cf7_127.0.0.1_ok.yml', record_mode='new_episodes')
def test_session_tasks_127_ok(app):
    rv = app.get('sessions/test3.yml/c8846a16-0c82-11e8-a65f-c48e8ff31cf7?host=127.0.0.1&status=OK')
    hosts = [b'127.0.0.1']
    tasks = [
                b'Gathering Facts',
                b'say hi',
                b'say hi 2',
                b'say hi 3',
                b'say hi 4',
                b'fail',
                b'change something'
            ]
    assert b'Host' in rv.data
    assert b'Ok' in rv.data
    assert b'Failures' in rv.data
    assert b'Unreachable' in rv.data
    assert b'Changed' in rv.data
    assert b'Skipped' in rv.data
    assert b'Timestamp' in rv.data
    assert b'c8846a16-0c82-11e8-a65f-c48e8ff31cf7' in rv.data
    for host in hosts:
        assert host in rv.data
    for task in tasks:
        assert task in rv.data, "All tasks should appear for 127"
    assert b'OK' in rv.data

@vcr.use_cassette('tests/vcr_cassettes/pages/c8846a16-0c82-11e8-a65f-c48e8ff31cf7_localhost_failed.yml', record_mode='new_episodes')
def test_session_tasks_localhost_failed(app):
    rv = app.get('sessions/test3.yml/c8846a16-0c82-11e8-a65f-c48e8ff31cf7?host=localhost&status=FAILED')
    hosts = [b'localhost']
    excluded_tasks = [
                b'Gathering Facts',
                b'say hi',
                b'say hi 2',
                b'say hi 3',
                b'say hi 4',
                b'change something'
            ]
    included_tasks = [
                b'fail',
            ]
    assert b'Host' in rv.data
    assert b'Ok' in rv.data
    assert b'Failures' in rv.data
    assert b'Unreachable' in rv.data
    assert b'Changed' in rv.data
    assert b'Skipped' in rv.data
    assert b'Timestamp' in rv.data
    assert b'c8846a16-0c82-11e8-a65f-c48e8ff31cf7' in rv.data
    for host in hosts:
        assert host in rv.data
    for task in included_tasks:
        assert task in rv.data
    for task in excluded_tasks:
        assert task not in rv.data
    assert b'FAILED' in rv.data

@vcr.use_cassette('tests/vcr_cassettes/pages/c8846a16-0c82-11e8-a65f-c48e8ff31cf7_localhost_ok.yml', record_mode='new_episodes')
def test_session_tasks_localhost_ok(app):
    rv = app.get('sessions/test3.yml/c8846a16-0c82-11e8-a65f-c48e8ff31cf7?host=localhost&status=OK')
    hosts = [b'localhost']
    included_tasks = [
                b'Gathering Facts',
                b'say hi',
                b'say hi 2',
                b'say hi 3',
                b'say hi 4',
                b'change something'
            ]
    excluded_tasks = [
                b'fail',
            ]
    assert b'Host' in rv.data
    assert b'Ok' in rv.data
    assert b'Failures' in rv.data
    assert b'Unreachable' in rv.data
    assert b'Changed' in rv.data
    assert b'Skipped' in rv.data
    assert b'Timestamp' in rv.data
    assert b'c8846a16-0c82-11e8-a65f-c48e8ff31cf7' in rv.data
    for host in hosts:
        assert host in rv.data
    for task in included_tasks:
        assert task in rv.data
    for task in excluded_tasks:
        assert task not in rv.data
    assert b'OK' in rv.data

@vcr.use_cassette('tests/vcr_cassettes/pages/c8846a16-0c82-11e8-a65f-c48e8ff31cf7_all_ok.yml', record_mode='new_episodes')
def test_session_tasks_all_ok(app):
    rv = app.get('sessions/test3.yml/c8846a16-0c82-11e8-a65f-c48e8ff31cf7?status=OK')
    hosts = [b'localhost', b'127.0.0.1']
    included_tasks = [
                b'Gathering Facts',
                b'say hi',
                b'say hi 2',
                b'say hi 3',
                b'say hi 4',
                b'fail',
                b'change something'
            ]
    assert b'Host' in rv.data
    assert b'Ok' in rv.data
    assert b'Failures' in rv.data
    assert b'Unreachable' in rv.data
    assert b'Changed' in rv.data
    assert b'Skipped' in rv.data
    assert b'Timestamp' in rv.data
    assert b'c8846a16-0c82-11e8-a65f-c48e8ff31cf7' in rv.data
    for host in hosts:
        assert host in rv.data
    for task in included_tasks:
        assert task in rv.data
    assert b'OK' in rv.data

@vcr.use_cassette('tests/vcr_cassettes/pages/c8846a16-0c82-11e8-a65f-c48e8ff31cf7_all_failed.yml', record_mode='new_episodes')
def test_session_tasks_all_failed(app):
    rv = app.get('sessions/test3.yml/c8846a16-0c82-11e8-a65f-c48e8ff31cf7?status=FAILED')
    hosts = [b'localhost', b'127.0.0.1']
    excluded_tasks = [
                b'Gathering Facts',
                b'say hi',
                b'say hi 2',
                b'say hi 3',
                b'say hi 4',
                b'change something'
            ]
    included_tasks = [
                b'fail',
            ]
    assert b'Host' in rv.data
    assert b'Ok' in rv.data
    assert b'Failures' in rv.data
    assert b'Unreachable' in rv.data
    assert b'Changed' in rv.data
    assert b'Skipped' in rv.data
    assert b'Timestamp' in rv.data
    assert b'c8846a16-0c82-11e8-a65f-c48e8ff31cf7' in rv.data
    for host in hosts:
        assert host in rv.data
    for task in included_tasks:
        assert task in rv.data
    assert b'FAILED' in rv.data
