import time
from rousette.models import load_all_scorers
from test.fixtures import *

def test_submit_doc(client, config, doc_queue):
    client.post("/docs", json={"doc_id": "source1/doc1", "body": "the quick brown fox jumped over the lazy dog"})
    doc = doc_queue.get_by_id("source1/doc1")
    assert doc['the'] == 2
    assert doc['quick'] == 1


@pytest.fixture
def basic_data(doc_queue, parser):
    doc_queue.put("source1/doc1", parser("the quick brown fox jumped over the lazy dog"))
    doc_queue.put("source1/doc2", parser("the quick brown fox jumped over the lazy fox"))


def test_load_doc(client, basic_data):
    resp = client.get("/docs/source1/doc1/repr")
    assert resp.status_code == 200
    doc = resp.json['doc']
    assert doc['the'] == 2
    assert doc['quick'] == 1
    assert doc['fox'] == 1
    resp = client.get("/docs/source1/doc2/repr")
    assert resp.status_code == 200
    doc = resp.json['doc']
    assert doc['fox'] == 2
    resp = client.get("/docs/source2/doc1/repr")
    assert resp.status_code == 404


def test_get_vectorized_doc(client, docs, model, scorer):
    for doc_id, doc in docs:
        resp = client.get(f"/docs/{doc_id}/vector/{model}")
        assert resp.status_code == 200

def test_build_model(config, client, docs, populated_queue):
    resp = client.post("/models", json={"num_topics": 3})
    assert resp.status_code == 201
    model_id = resp.json['model_id']
    assert model_id in load_all_scorers(config)