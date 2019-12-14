import pytest
import rousette
from test import test_config
from rousette.queue import get_queue
from rousette.doc_parser import get_parser

@pytest.fixture
def config_def():
    return test_config

@pytest.fixture
def app(config_def):
    return rousette.create_app(config_def)

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture
def config(app):
    return app.config

@pytest.fixture
def queue(config):
    return get_queue(config)

@pytest.fixture
def parser(config):
    return get_parser(config)