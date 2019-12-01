import pytest
import rousette
from rousette.env import get_queue
from test import test_config

@pytest.fixture
def config():
    return test_config

@pytest.fixture
def client(config):
    with rousette.create_app(config).test_client() as client:
        yield client

def test_submit_doc(client):
    client.post("/docs", json={"doc_id": "doc1", "body": "the quick brown fox jumped over the lazy dog"})
    doc = get_queue().get_doc("doc1")
    assert doc['the'] == 2
    assert doc['quick'] == 1

def test_load_doc(client):
    get_queue().submit_doc("doc1", "the quick brown fox jumped over the lazy dog")
    resp = client.get("/docs/doc1")
    assert resp.status_code == 200
    doc = resp.json['doc']
    assert doc['the'] == 2
    assert doc['quick'] == 1