from flask import Flask, request, jsonify, make_response
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
    loc = f"/docs/{doc_id}"
    return jsonify(location=loc), 201, {"Location": loc}

@app.route("/docs/<path:doc_id>")
def get_doc(doc_id):
    queue = get_queue()
    data = queue.get_doc(doc_id)
    return jsonify(doc=data)