import json
from flask import Flask, request
from rousette.env import get_queue

app = Flask(__name__)

@app.route("/docs", methods=["POST"])
def submit_doc():
    """
    Submit a document
    """
    queue = get_queue()
    doc_id = request.json['doc_id']
    body = request.json['body']
    queue.submit_doc(doc_id, body)
    return 201

@app.route("/docs/<path:doc_id>")
def get_doc(doc_id):
    queue = get_queue()
    data = queue.get_doc(doc_id)
    return 200, json.dumps(data)