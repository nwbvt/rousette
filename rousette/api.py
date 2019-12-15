from flask import Flask, request, jsonify, make_response
from rousette.queue import get_doc_queue, get_vec_queue
from rousette.doc_parser import get_parser

app = Flask(__name__)

@app.route("/docs", methods=["POST"])
def submit_doc():
    """
    Submit a document
    """
    queue = get_doc_queue(app.config)
    parser = get_parser(app.config)
    doc_id = request.json['doc_id']
    body = request.json['body']
    doc = parser(body)
    queue.put(doc_id, doc)
    loc = f"/docs/{doc_id}"
    return jsonify(location=loc), 201, {"Location": loc}

@app.route("/docs/<path:doc_id>/repr")
def get_doc(doc_id):
    queue = get_doc_queue(app.config)
    data = queue.get_by_id(doc_id)
    if data:
        return jsonify(doc=data)
    return jsonify(err=f"{doc_id} not found"), 404

@app.route("/docs/<path:doc_id>/vector/<int:model_id>")
def get_doc_vector(doc_id, model_id):
    queue = get_vec_queue(app.config)
    data = queue.get_by_id((doc_id, model_id))
    if data is not None:
        return jsonify(doc=data.tolist())
    return jsonify(err=f"{doc_id} not found"), 404