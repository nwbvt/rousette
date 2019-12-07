import pytest
import rousette
from rousette.queue import get_queue
from test import test_config

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

def test_submit_doc(client, config, queue):
    client.post("/docs", json={"doc_id": "source1/doc1", "body": "the quick brown fox jumped over the lazy dog"})
    doc = queue.get_doc("source1/doc1")
    assert doc['the'] == 2
    assert doc['quick'] == 1

def test_load_doc(client, config, queue):
    queue.submit_doc("source1/doc1", "the quick brown fox jumped over the lazy dog")
    resp = client.get("/docs/source1/doc1/repr")
    assert resp.status_code == 200
    doc = resp.json['doc']
    assert doc['the'] == 2
    assert doc['quick'] == 1
    resp = client.get("/docs/source2/doc1/repr")
    assert resp.status_code == 404