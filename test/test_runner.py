import requests
from test.fixtures import bat_doc, bird_doc, dog_doc
import argparse
import random

def run():
    parser = argparse.ArgumentParser("script to generate documents")
    parser.add_argument("--length", type=int, help="Doc length")
    parser.add_argument("--num_docs", type=int, help="Number of docs")
    parser.add_argument("--host", default="http://127.0.0.1:5000", help="Base URL of api")
    args = parser.parse_args()
    for i in range(args.num_docs):
        doc_func = random.choice([bat_doc, bird_doc, dog_doc])
        doc = doc_func(args.length)
        resp = requests.post(f"{args.host}/docs", json={"doc_id": f"sample/doc_{i}", "body": doc})
        assert resp.status_code//100 == 2


if __name__ == "__main__":
    run()