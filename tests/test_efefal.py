import vcr

@vcr.use_cassette('tests/vcr_cassettes/pages/index.yml')
def test_playbook_index(app):
    rv = app.get('/')
    assert b'test.yml' in rv.data
    assert b'test2.yml' in rv.data
    assert b'test3.yml' in rv.data
    assert b'<li><a href="/sessions/test2.yml"> test2.yml</li>' in rv.data

@vcr.use_cassette('tests/vcr_cassettes/pages/test3.yml')
def test_runs(app):
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

@vcr.use_cassette('tests/vcr_cassettes/pages/a5cba87a-0a0e-11e8-b454-c48e8ff31cf7.yml')
def test_run_tasks(app):
    rv = app.get('sessions/test3.yml/a5cba87a-0a0e-11e8-b454-c48e8ff31cf7')
    hosts = [b'127.0.0.1', b'localhost']
    tasks = [
                b'TASK: Gathering Facts',
                b'TASK: say hi',
                b'TASK: say hi 2',
                b'TASK: say hi 3',
                b'TASK: say hi 4',
                b'TASK: fail',
                b'TASK: change something'
            ]
    assert b'Host' in rv.data
    assert b'Ok' in rv.data
    assert b'Failures' in rv.data
    assert b'Unreachable' in rv.data
    assert b'Changed' in rv.data
    assert b'Skipped' in rv.data
    assert b'Timestamp' in rv.data
    assert b'a5cba87a-0a0e-11e8-b454-c48e8ff31cf7' in rv.data
    for host in hosts:
        assert host in rv.data
    for task in tasks:
        assert task in rv.data
