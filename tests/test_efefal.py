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
    print(rv)

