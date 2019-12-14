from test.fixtures import *

def test_submit_load_doc(client, config, doc_queue):
    client.post("/docs", json={"doc_id": "source1/doc1", "body": "the quick brown fox jumped over the lazy dog"})
    doc = doc_queue.get_by_id("source1/doc1")
    assert doc['the'] == 2
    assert doc['quick'] == 1
    resp = client.get("/docs/source1/doc1/repr")
    assert resp.status_code == 200
    doc = resp.json['doc']
    print(doc)
    assert doc['the'] == 2
    assert doc['quick'] == 1
    resp = client.get("/docs/source2/doc1/repr")
    assert resp.status_code == 404