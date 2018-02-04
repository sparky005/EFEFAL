import efefal
from efefal.efefal import create_app
import pytest
import vcr

@pytest.fixture
def app():
    config = { 'TESTING': True }
    app = create_app(config)
    app.testing = True
    app = app.test_client()
    return app

def test_playbook_index(app):
    rv = app.get('/')
    assert b'test.yml' in rv.data
    assert b'test2.yml' in rv.data
    assert b'test3.yml' in rv.data

def test_runs(app):
    rv = app.get('/runs/test3.yml')
    assert b'SessionID' in rv.data
    assert b'Timestamp' in rv.data
    assert b'Playbook' in rv.data
    assert b'Ok' in rv.data
    assert b'Failed' in rv.data
    assert b'Unreachable' in rv.data
    assert b'Changed' in rv.data
    assert b'Skipped' in rv.data
    assert b'8262ba60-0930-11e8-8eaf-c48e8ff31cf7' in rv.data
    assert b'test3.yml' in rv.data

def test_run_tasks(app):
    rv = app.get('runs/tasks/test3.yml/8262ba60-0930-11e8-8eaf-c48e8ff31cf7')
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
    assert b'8262ba60-0930-11e8-8eaf-c48e8ff31cf7' in rv.data
    for host in hosts:
        assert host in rv.data
    for task in tasks:
        assert task in rv.data
